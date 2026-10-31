# Reminders for the owner

Kept by the Claude web chat. This is not an EX message and is not reviewed; ChatGPT does not need it.
Claude raises each OPEN item when its "when" arrives, or whenever the owner asks. An item is marked
DONE (with the date and where it was settled) or DROPPED (with the reason); items are never deleted.
Dates are Adelaide dates. US-ASCII, CRLF.

## R-001  The owner's two further methods, and the add-a-method process

- Asked: 29 October 2026 ("I have 2 more I'd like considered later"; discuss the process for adding
  new methods).
- Status: OPEN.
- What: the owner's two further method ideas, confirmed by the owner on 30 October 2026 as
  Methods A and B in doc/GASI_thought_experiments/Proposal_Methods_A_and_B_FROM_GAIS_v0.1.md, which
  supersedes the pre-exploratory GASI_thought_experiments_possibly_unexplored_areas.md:
  A, recurrence-gap spectrum (does a number that has just been drawn repel or cluster?);
  B, delay-embedding analogues (predict from what followed the past draws that looked most like
  the recent ones; also look for up/down patterns that never occur).
- R2 already lists close relatives: A is near E_17 (Discrete Recurrence Hazard Curves, also E_19);
  B is near E_45 (Delay-Embedded Nearest-Analogue Forecast, also E_27 and E_32). A and B are to
  become those methods' specifications rather than new E-numbers.
- Progress: the add-a-method process exists (the new-method template, used for E_6 and E_3/E_4).
- When (owner's revised order, 30 October 2026): A in wave 2 (with E_2, E_19, E_18), right after the
  first light counting methods; B in wave 3 (with E_27), after releases and WF-1.

## R-002  Pattern-spotting by non-local means (the NLMEANS idea)

- Asked: 30 October 2026.
- Status: OPEN (postponed by the owner, 30 October 2026).
- What: discuss, even if only to record why it is set aside, whether non-local means (NL-means, an
  image denoising method that averages each pixel with others anywhere in the image whose
  surrounding patches look alike) or a similar "non-local" technique could say anything about the
  draws. Ideas to discuss:
  - viewing the draw history in different ways: as a series of images over time, as one large image
    (draws by numbers, for example), or other imaginative arrangements;
  - applying NL-means or similar to those views, and seeing whether any structure (edges, repeated
    patches, anything) emerges that fair draws would not produce;
  - whether any such structure could be turned into a testable way of ranking numbers for the next
    draw;
  - whether it suggests some other oddball method that is easy to code.
  The owner's own view: probably not feasible, but worth discussing and recording either way.
- When (owner's revised order, 30 October 2026): straight after wave 3 (Method B), or whenever the
  owner asks. Any method it yields joins a later wave.

## R-003  Optional tidy-up of old EX copies in review/

- Asked: offered by Claude on 29 October 2026 (after the DOC-6 install).
- Status: OPEN (optional; nothing depends on it).
- What: review/ holds 10 older EX copies (EX_026 twice, EX_027 to EX_034), all identical to the
  copies in exchange/ (apart from line endings in the .md files). The owner may remove them with
  one git rm commit; Claude would give the exact commands and check the result.
- When: whenever convenient.

## R-004  The NIST Randomness Beacon root for the first stochastic method

- Asked: 30 October 2026 ("we had talked about a NIST seed ... when do we do that?").
- Status: OPEN.
- What: decisions D-9 to D-11 (owner, 28 October 2026; in the register) say a seed policy's root is one
  pre-announced NIST Randomness Beacon pulse, fetched once by the owner by hand and checked
  independently; runs never fetch it. Roots may be switched as a new revision or variant, and every root
  tried is logged and counted. For development runs on past draws, a pulse published afterwards may be
  used, labelled as experiment randomisation; a real forecast needs a root approved beforehand.
- Not needed yet: E_1, E_6, E_3 and E_4 are deterministic and use no random numbers.
- Steps when due: the method's design note includes its seed policy; the owner picks a future pulse
  time, recorded before it arrives; after it is published, the owner fetches it in a browser and gives
  it to Claude; Claude checks it, and it goes into the register.
- Progress (30 October 2026): the releases and WF-1 design note v0.1 (EX_077, section 8.1) announces
  the pulse: NIST Beacon 2.0, chain 2, timeStamp 2026-11-06T00:00:00.000Z (10:30 am Adelaide, Friday
  6 November), field outputValue. The owner may pick another later minute before that one arrives
  (decision WF1-9). After that time: open
  https://beacon.nist.gov/beacon/2.0/pulse/time/1793923200000 in the browser, save the JSON to
  E:\TEMP and attach it to the Claude chat.
- When: at WF-1's design (owner decision W2-8, 30 October 2026). Wave 2 uses no random numbers; R3's
  N1 fair-draw simulator, used at WF-1, is the first part that does. Method A's later diagnostics,
  Method B's simulated checks and wave 9's machine learning also use random numbers.

## R-005  E_1 revision 2 (real-capable), with CODE-3 first

- Asked: 31 October 2026 (owner decision WF1-13, option C, while WF-1A was being coded).
- Status: OPEN. Design v0.1 sent for review in EX_086 (31 October 2026). Owner choices before review:
  ER-1 to ER-4 as recommended (one package; install and release together in two separate steps; r1
  archived complete; the adapter docstring corrected); ER-6 (an E_1-only batch plan) declined.
  EX_087: RECHECK (B01: the install's interim was not fail-closed; C01, C02, O01). v0.1r1 sent in
  EX_088; the owner chose ER-2r1 (one package, five steps behind a temporary E_1 flag).
  EX_089: B01, C01, C02 resolved; new C03 (exact refusal codes in the barrier test). v0.1r2 sent in
  EX_090 for a focused RECHECK.
  EX_091: PASS (O03 optional: T09's step-0 planning wording, applied in the code's test).
  OWNER-RATIFIED 31 October 2026: design v0.1r2 (LF fb3b26da...209a) as reviewed. Coding started the
  same day, in parallel with the REL-1 and WF-1A installs; it installs after WF-1A.
  Code candidate E1R2_Install_v1 sent for R-2 review in EX_092 (31 October 2026): 348 tests on both
  Pythons, 16/16 mutations, rehearsals PASS. Register v0.22 follows after the REL-1 and WF-1A installs.
- What: E_1 revision 1's multi-game function refuses real data (kept unchanged on purpose when E_1 was
  wired into the contract), so E_1 cannot run in WF-1's walk-forward batches. The owner chose a new
  revision, E_1 r2, which accepts real development runs, with E_1's legacy runner moved to r2 too.
  Needs: CODE-3 (retirement tooling: r1 moves to archive/methods/E_001/r1/, decision D-5) first; a short
  E_1 r2 design note; the r2 declaration and registry entries (installed unreleased, then released); the
  legacy runner's release check (D2-3) and E_1's goldens reviewed for r2.
- Interim: WF-1A names E_1 in each batch plan as not in the cohort, with the reason; families have 78
  tracks until E_1 r2 joins. Then a new batch over the full cohort (40 variants, about 105 minutes
  for Powerball) gives one complete batch per game to score.
- When: after the REL-1 and WF-1A packages, before or alongside WF-1B, so E_1 can be in the first report.

## R-006  Deferred performance study (the very last stage)

- Asked: 31 October 2026 (the owner scheduled it; "need not read nor consider it now, only schedule it").
- Status: SCHEDULED, NOT ACTIVE. Nothing to do until the owner activates it.
- What: the owner's proposal doc/Deferred_Performance_Engineering_Proposal_v0_1.md (v0.1, committed
  by the owner at 1050338): a profiling-first study of where the time goes, then a decision on any
  speed-up, under the project's usual review and owner gates.
- When: at the very end of the project, after all implementation and clean-up (roadmap item 22).
- Record: the next register edition lists the proposal as owner-committed and unreviewed, with this
  stage as scheduled only; no review is asked for now.

## Standing reminders

- Show the owner where the project is up to (exchange/OWNER_ROADMAP.md) at each milestone, and
  whenever asked.
- Save every downloaded ZIP to E:\TEMP, never into the repository (the browser defaults to review/).
