# Joint ChatGPT-Claude working principle: main-game priority, proportional engineering and minimum overhead

**Status: AGREED** by Claude (designer and coder) and the ChatGPT reviewer on 18 November 2026, on text proposed by the
project owner (hydra3333) at 00:11 Australia/Adelaide. Recorded by Claude at 00:22 the same day (decision log entry 81).

**How it was agreed.** The owner proposed the text. Claude agreed and proposed three small additions. The reviewer
accepted all three, with one wording refinement to the third, which Claude accepts. The three additions are marked
"[addition 1]" to "[addition 3]" below. Everything else is the owner's text, transcribed in plain ASCII.

**What it is not.** It creates no new approval process and no new governance. It does not reduce reporting to the owner,
detailed technical exchanges or independent review. It supersedes nothing: the owner's rules in decision log entries 78
and 80 stand, and this principle is the shared wording for them.

## The principle

Our shared objective is to maximise progress on the predictive-randomness research, not to maximise the completeness or
sophistication of the surrounding software and procedures.

The main game is investigating whether methods can predict physical lottery outcomes, implementing and experimenting with
those methods, producing correctly frozen forecasts, scoring them accurately, evaluating the evidence scientifically, and
making the system practical to use.

Minimum overhead means minimising low-value engineering effort, not minimising communication, documentation or
independent review.

We agree to apply the following principles:

1. **Prioritise by scientific and practical value.** Before proposing additional code, checks, tests, safeguards or
   procedures, consider their likely contribution to the project's objectives, the probability and consequences of the
   problem being addressed, and their cost in development, testing and review effort.

2. **Maintain rigorous correctness where it matters.** Protect scientific validity, strict N-1 isolation, frozen forecast
   integrity, correct scoring, statistical inference, correct implementation of each software method and calculation
   against its specification, accurate and traceable reporting of results from their underlying validated records
   (including sealed records where applicable), and clear identification of what was and was not tested, [addition 3]
   immutable experimental evidence, reproducibility, consequential data integrity and operational safety. Unconventional
   research and exploratory reruns remain legitimate project objectives.

3. **Avoid peripheral perfectionism.** A theoretical edge case, unusual environmental condition or conceivable failure
   does not automatically justify elaborate handling, extensive tests or additional procedures. For low-probability,
   low-consequence situations, prefer a simple safe response, including an informative refusal where appropriate. Do not
   construct elaborate recovery mechanisms without a material benefit.

4. **Keep complexity proportionate.** Prefer reusing existing mechanisms and straightforward solutions over new
   abstractions, registries, defensive layers or administrative machinery. Additional complexity needs a demonstrable
   benefit proportionate to its cost.

5. **Preserve independent technical judgment.** Claude should implement proportionate solutions; ChatGPT should
   independently assess their correctness, value and complexity. Both must challenge unnecessary engineering, including
   their own suggestions. Finding an imperfection is not, by itself, a reason to demand a correction.

6. **Preserve communication and authority.** Detailed technical exchanges are welcome and encouraged when useful. The
   owner should be involved in consequential decisions, not routine implementation trivia. Existing owner-GO requirements
   and independent-review rights remain intact. This agreement creates no new approval process.

**Practical test.** Before expanding the work, ask: what meaningful scientific, operational or safety problem does this
address? How likely and consequential is it, and is the proposed effort proportionate to the benefit?

Whoever proposes the extra work states the concrete failure and its consequence in a sentence or two. If that cannot be
stated, the item is simplified, deferred or dropped. [addition 1]

If the contribution is marginal, simplify, defer or omit it. If the consequences are substantial, give it the engineering
and review attention it deserves.

**Application to MHUP-B.** OV-1 arithmetic, pre-outcome evidence, leakage prevention and correct scoring warrant deep
scrutiny. Routine date/time calculations warrant ordinary correctness and simple automated checks, not an extended
engineering programme. Existing validated code need not be removed merely because we would choose a simpler approach
today.

Where an item of a ratified plan or design looks disproportionate when it comes to be built, Claude builds the simplest
version that satisfies the ratified rule and says so in the slice's covering note; removing or changing a ratified rule
still needs the owner. [addition 2]

This is a project-wide prioritisation principle, not a reduction in scientific standards. Its purpose is to prevent
low-value technical work from consuming the time, attention and resources needed for the actual research.

Claude and ChatGPT should identify any substantive disagreement with this principle, resolve it between themselves where
within their authority, and present only consequential unresolved choices to the owner. Once agreed, apply it
consistently throughout future implementation and review.

## Agreed notes on applying it

- **The owner's clarification (00:15).** The science, the software methods, the calculations and the reporting all have
  to be right. Addition 3 puts that into principle 2. The objective is proportionate engineering effort, never
  approximate science or calculations (the reviewer's words, which Claude shares).
- **Slice 2, the missed-week rule (the reviewer's note, accepted by Claude).** The missed-week eligibility rule is part of
  OV-1's scientific validity, so it is implemented correctly and tested sufficiently to support the statistical claim.
  That does not justify elaborate recovery machinery or exhaustive testing of peripheral operational scenarios.
- **Slice 2, how Claude will apply it.** Full depth for OV-1 arithmetic, pre-outcome evidence, the missed-week rule,
  leakage prevention and scoring. The plain version, with few tests, for restart corner cases and development-run
  plumbing; unusual operational paths get a refusal that says why.
