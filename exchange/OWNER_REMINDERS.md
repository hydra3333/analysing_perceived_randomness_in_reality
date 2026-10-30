# Reminders for the owner

Kept by the Claude web chat. This is not an EX message and is not reviewed; ChatGPT does not need it.
Claude raises each OPEN item when its "when" arrives, or whenever the owner asks. An item is marked
DONE (with the date and where it was settled) or DROPPED (with the reason); items are never deleted.
Dates are Adelaide dates. US-ASCII, CRLF.

## R-001  The owner's two further methods, and the add-a-method process

- Asked: 29 October 2026 ("I have 2 more I'd like considered later"; discuss the process for adding
  new methods).
- Status: OPEN.
- What: consider the owner's two further method ideas. Probably Methods A and B in
  doc/GASI_thought_experiments/Proposal_Methods_A_and_B_FROM_GAIS_v0.1.md:
  A, recurrence-gap spectrum (does a number that has just been drawn repel or cluster?);
  B, delay-embedding analogues (predict from what followed the past draws that looked most like
  the recent ones; also look for up/down patterns that never occur). The owner to confirm.
- Progress: the add-a-method process now exists in draft (the new-method template, first used for
  E_6 and then for E_3/E_4).
- When: after the E_3/E_4 review passes, at the next method-design round.

## R-002  Pattern-spotting by non-local means (the NLMEANS idea)

- Asked: 30 October 2026.
- Status: OPEN.
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
- When: in the same method-design round as R-001, or whenever the owner asks.

## R-003  Optional tidy-up of old EX copies in review/

- Asked: offered by Claude on 29 October 2026 (after the DOC-6 install).
- Status: OPEN (optional; nothing depends on it).
- What: review/ holds 10 older EX copies (EX_026 twice, EX_027 to EX_034), all identical to the
  copies in exchange/ (apart from line endings in the .md files). The owner may remove them with
  one git rm commit; Claude would give the exact commands and check the result.
- When: whenever convenient.

## Standing reminder

- Save every downloaded ZIP to E:\TEMP, never into the repository (the browser defaults to review/).
