# Where the project is up to (the owner's roadmap)

Kept by the Claude web chat; updated at each milestone. Plain English. This is a working list, not
reviewed and not part of the rules: the ratification register is the record. US-ASCII, CRLF.
Last updated: 30 October 2026, after the handovers were installed (step 7 done).

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

## Next, in the owner's order

7.  DONE - Refreshed the two handovers (Claude's H-1 v1r5, ChatGPT's H-2 v1r6) and register v0.17,
           installed at 8defe9d. A handover is the briefing a new chat reads to take over the work.
8.  NOW  - The template, draft 2: adds what E_3/E_4 taught (shared helpers, methods that give scores
           but no probabilities, a minimum number of past draws).
9.  NEXT - The E_7 to E_16 batch, built from the template. These ten catalogue methods are the
           "frequency, Bayesian and regime" family: more ways of estimating how likely each number
           is from how often it has come up (E_7 to E_10: shrinking towards fair, a shared
           "family" estimate, faster forgetting, short-versus-long-term contrasts), and ways of
           spotting whether behaviour changes between periods (E_11 to E_13: change points, hidden
           states, slow drift; E_14: calendar effects; E_15: eras; E_16: a slightly biased urn).
           Some (E_12, E_13) may be heavy enough to need their own package; that is decided at
           design. The NIST seed (reminder R-004) is settled here if any of them uses random numbers.
10. NEXT - Method A as E_17. Method A is the first of your two ideas (from the GASI proposal): does
           a number that has just been drawn tend to stay away for a while, or come back sooner,
           than fair draws allow? The catalogue already has a slot for that idea, E_17 "Discrete
           Recurrence Hazard Curves", so Method A becomes E_17's exact rule rather than a new method
           number. It ranks numbers by their chance of appearing next, given how long since they
           were last drawn.
11. NEXT - Method B as E_45. Method B is your second idea: find the past weeks whose recent run of
           draws looked most like the latest run, and predict from what came next after them; also
           look for up/down patterns that never occur. Its catalogue slot is E_45 "Delay-Embedded
           Nearest-Analogue Forecast".
12. NEXT - Discuss the NL-means idea (reminder R-002): whether an image-style "non-local" method
           could find repeated patches in the draw history.

## Later (each its own package and decision)

- Releases: switch methods on, one at a time (E_6's remember-everything version first). Even then
  they run only on invented test data until WF-1.
- WF-1: real-data runs over past draws (walk-forward: for each past draw, predict it from the draws
  before it only, then score), and the scorer that measures them.
- The rest of the catalogue (E_2, E_5, E_18 onward).
- Holdout testing (the sealed draws), and then real next-draw predictions from all methods together.
