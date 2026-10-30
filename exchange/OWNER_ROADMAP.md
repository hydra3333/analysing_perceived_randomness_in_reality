# Where the project is up to (the owner's roadmap)

Kept by the Claude web chat; updated at each milestone. Plain English. This is a working list, not
reviewed and not part of the rules: the ratification register is the record. US-ASCII, CRLF.
Last updated: 30 October 2026, after E_3/E_4 were installed.

## How every package goes (the routine)

1. Claude writes the design; ChatGPT reviews it; the owner decides.
2. Claude writes the code and tests; ChatGPT reviews them; the owner ratifies.
3. Claude Code rehearses the install on the owner's machine, in a throw-away copy.
4. The owner installs (check, copy, check, tests, commit, check, push).
5. Claude checks the result from GitHub; the next register edition records it.

## Done

1. DONE - The plan and specifications (proposal, architecture, method list R2, measuring rules R3),
   the safe launcher and coordinator, and the results-data tools.
2. DONE - The method "contract": the shared rules every new method plugs into (CODE-1, CODE-2).
3. DONE - Claude Code set up as the local runner; it rehearses every install.
4. DONE - E_6, per-number Beta-Bernoulli with optional forgetting: installed, not yet runnable.
5. DONE - The new-method template, draft 1 (doc/METHOD_TEMPLATE/), installed with E_6.
6. DONE - E_3 and E_4, polynomial curve fits (value and slope): installed, not yet runnable.

## Next, in the owner's order

7.  NOW  - Refresh the two handovers (Claude's H-1, ChatGPT's H-2) and register v0.17.
8.  NEXT - The template, draft 2: adds what E_3/E_4 taught (shared helpers, score-only methods,
           minimum history).
9.  NEXT - The E_7 to E_16 batch (frequency, Bayesian and regime methods), built from the template.
           The NIST seed (reminder R-004) is settled here if any of them uses random numbers.
10. NEXT - Method A (recurrence-gap spectrum), as E_17.
11. NEXT - Method B (delay-embedding analogues), as E_45.
12. NEXT - Discuss the NL-means idea (reminder R-002).

## Later (each its own package and decision)

- Releases: switch methods on, one at a time (E_6 full memory first). Even then they run only on
  invented test data until WF-1.
- WF-1: real-data runs over past draws (walk-forward), and the scorer that measures them.
- The rest of the R2 list (E_2, E_5, E_18 onward).
- Holdout testing (the sealed draws), and then real next-draw predictions from all methods together.
