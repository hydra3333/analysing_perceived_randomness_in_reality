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
- When: at WF-1's design (owner decision W2-8, 30 October 2026). Wave 2 uses no random numbers; R3's
  N1 fair-draw simulator, used at WF-1, is the first part that does. Method A's later diagnostics,
  Method B's simulated checks and wave 9's machine learning also use random numbers.

## Standing reminders

- Show the owner where the project is up to (exchange/OWNER_ROADMAP.md) at each milestone, and
  whenever asked.
- Save every downloaded ZIP to E:\TEMP, never into the repository (the browser defaults to review/).
