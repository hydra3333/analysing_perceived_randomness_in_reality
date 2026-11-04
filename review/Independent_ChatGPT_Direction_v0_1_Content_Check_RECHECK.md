## Independent reviewer — Operational Direction v0.1

Verdict: RECHECK — focused document corrections, not a change of direction.

I've reviewed the complete `Direction_for_operational_procedures_v0_1.md`, the owner's ratification at the end of stock-take v0.7, the ratification register v0.23 and H-1 v1r7.

The document successfully captures your intended operational workflow and is suitable as a plain-English direction statement. I support installing it in `doc/` once the points below are corrected.

However, I found one substantive classification error, several statements that exceed what has been decided, and a few binding protections that deserve explicit mention.

### 1. Powerball 1587 and 1588 are incorrectly classified as CATCH-UP

CORRECTION — required

Section 3 says:

> Powerball 1585, 1586 (Mode H) and 1587, 1588 (catch-up) also carry an exposure flag.

The problem is the unconditional CATCH-UP label.

Under MH-1, a forecast made after its draw qualifies as CATCH-UP only when the method revision was already installed before that draw. The current cohort was released on 31 October 2026; draws 1587 and 1588 predate that release. Consequently, retrospective evaluations for those draws by the current cohort are development evidence, not qualifying CATCH-UP results.

The owner's subsequent ratification explicitly identifies Powerball 1590 and Oz Lotto 1707 onward as potentially eligible for CATCH-UP, subject to the local installation evidence.

The exposure flags still apply, and those draws remain valid and counted. Only their evidence classification needs correcting.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://raw.githubusercontent.com\&sz=32)

GitHub+1



Suggested replacement:

> Powerball 1585 and 1586 carry exposure flags within Mode H. Powerball 1587 and 1588 are post-holdout draws and also carry exposure flags when evaluated. Their results are classified according to the method's installation date; for the current cohort, retrospective evaluations of 1587 and 1588 are development evidence, not CATCH-UP. All flagged draws remain valid and counted.

### 2. Q5 is more settled than the direction document acknowledges

CORRECTION — required

Section 3 and section 11 describe the local installation record primarily as an intended answer to an open question.

The owner has now specifically ratified the mechanism: a create-only local installation record, including a one-off owner-confirmed record for the existing cohort. The detailed implementation and verification rules remain for the design.

Suggested replacement:

> The owner has decided that installation eligibility is established using create-only local installation records, not Git history, including a one-off owner-confirmed record for the existing cohort (owner decision, 2 November 2026; OFF-1). The exact record format, verification and recovery rules remain open for the design.

Section 11 should similarly distinguish Q5's decided mechanism from its still-open implementation details.

### 3. Mode H is not equivalent to a genuine prospective forecast

CORRECTION — required

Section 4 states that Mode H uses the same engine and guarantees as the weekly process. That is too strong while Q1 remains open.

Under option A, forecasts can be produced after the holdout outcomes have entered the system, albeit with strict N−1 data isolation. The method's precommitted code and study plan provide safeguards, but the forecasts do not have the same pre-draw standing as genuine prospective forecasts.

Suggested replacement:

> Mode H is intended to rehearse the forecasting, scoring and data-isolation mechanics used by the weekly process. Under option A it is a precommitted holdout evaluation, not genuine pre-draw forecasting. Its precise guarantees and implementation remain subject to the independent design review and owner approval.

I accept the owner's preference for A as an input to the review. I do not regard Q1 as decided, and option B remains a legitimate alternative.

### 4. Several absolute statements need small qualifications

CORRECTION — required

These do not change the project's direction.

| Location                   | Issue and recommended clarification                                                                                                                                                                           |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Section 1 — dates          | Dates also matter for installation eligibility, audit records and forecast timing evidence. Draw numbers define the scientific sequence; dates are not used only for the two purposes stated.                 |
| Section 1 — every forecast | Not every method existed for every historical draw. Clarify that historical evaluations are generated for eligible method revisions and that later retrospective forecasts do not acquire prospective status. |
| Section 3 — PROSPECTIVE    | Freezing before the actual draw is not necessarily sufficient: Q4 may establish an earlier deadline. State that the forecast must meet the ratified prospective deadline.                                     |
| Section 5 — open forecast  | Say one open forecast per active variant per game, rather than merely per variant.                                                                                                                            |
| Section 5 — scoring        | "Nothing is scored twice" should mean no duplicate routine accepted scoring. Section 2 explicitly allows a separate, identified scoring run to correct a fault or introduce a new measure.                    |

These qualifications protect the owner's three-way distinction between immutable forecasts, preserved scoring evidence and refreshed reports.

### 5. Retirement wording is slightly over-restrictive

CORRECTION — recommended

Section 8 says:

> A method is retired only when superseded, never for performing badly.

The second part reflects the owner's principle that poorly performing methods remain visible.

However, "only when superseded" could prevent retirement for other legitimate reasons, such as an invalid implementation or an owner-directed administrative retirement.

I recommend:

> A method is never retired solely because it performs badly. Retirement for supersession or another legitimate reason follows the method-registry and archive rules. Historical evidence remains preserved and visible.

This keeps the scientific principle without introducing an unnecessarily absolute rule.

### 6. Preserve the execution gates and scientific limitations explicitly

CORRECTION — required before installation

The direction document is not supposed to reproduce H-1 or the full register. Nevertheless, because it describes commands the owner will eventually run, it needs a conspicuous statement that none of those commands is being authorised by the document.

H-1 explicitly keeps real-data runs, updates, holdout access, Mode H, FINAL, safety-switch changes and other protected actions behind separate owner approval.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://raw.githubusercontent.com\&sz=32)

GitHub



I recommend a short paragraph near the beginning:

> Status and authority: Owner-ratified operational direction, 2 November 2026. This is not an implementation specification or permission to execute any command, access the holdout or update results. The independently reviewed and owner-ratified designs, the method and process safety gates, and separate execution approvals remain binding. No real-data operation is authorised by this document.

That would also satisfy R-013's need for an intelligible status line once Claude adds the formal author, reviewer and installation metadata.

I recommend two further small adjustments: section 9 should clarify that an external witness proves timing only when its independently verifiable receipt is linked to the forecast digest; and section 4 should describe ten holdout draws as providing limited statistical power, rather than claiming they necessarily rule out large effects.

### 7. Plain-English readability

PASS

The document is substantially easier for the owner to understand than the technical design documents.

The sequencing is good: what exists, what remains immutable, labels, Mode H, weekly operation, missed weeks, new methods, retirements, offline operation and prerequisites.

The principal weakness is that identifiers such as R3, MH-1, OFF-1 and Q1 appear without explanation. A short sentence near the beginning would be enough:

> Codes such as MH-1 and OFF-1 identify previously recorded owner decisions; Q1 and similar labels identify questions still being resolved in the forthcoming design.

I would not expand this into a technical glossary.

## Additional observation — roadmap and reminders at `8982f61`

I inspected the updated roadmap and reminders on GitHub. They include the new direction-document reminder R-013 and deferred simplicity-review reminder R-014.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://raw.githubusercontent.com\&sz=32)

GitHub+1



R-013 is appropriate.

R-014 needs a small correction to preserve the owner's earlier instructions. The current wording schedules consideration after the first weekly sessions and highlights adding and retiring methods. The owner originally asked for the comprehensive KISS assessment after full implementation and follow-on work, only when explicitly requested. Its scope also includes the method registry, local experimentation without GitHub, excessive authentication and verification, and general operational simplicity.

I recommend expanding R-014 accordingly and retaining the owner's explicit activation requirement. It should not start automatically merely because the first weekly sessions have run.

## Final disposition

RECHECK — narrow document-content corrections.

I recommend that New Claude incorporate findings 1–6, retain the basic structure and plain-English tone, and provide the corrected candidate with an exact change list for a focused recheck.

The agreed 2 November owner decisions remain valid. My findings do not reopen them. In particular, I accept the three-way record distinction, archive-and-index retirement approach, status block, one-open-forecast invariant, locally recorded install evidence, and the revised planning target.

The 13–15 November 2026 timetable is an owner-agreed planning target, while FB-1 is the previously ratified protection against rushing. These should be labelled separately.

The resulting document should be an accessible explanation of the owner's intended operating model—not a substitute for the subsequent HIGH-risk design review.

No design, implementation, holdout access, results update or execution is approved by this content check. The next substantive scientific review remains EX_123 v0.1r1, after Claude's cold read and the owner's authorisation to submit it.