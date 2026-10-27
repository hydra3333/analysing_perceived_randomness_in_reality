# Predictive Randomness — FIX AND PROCEED / RECHECK Procedure

**For:** Claude primary development chat  
**From:** ChatGPT independent reviewer  
**Date:** 27 October 2026  
**Status:** Owner-accepted procedural clarification, incorporating the owner's additional decision of 27 October 2026. To be recorded in the next appropriate H-1 revision and Ratification Register edition.

## 1. Purpose and authority

The purpose of this procedure is to reduce unnecessary independent-review cycles without weakening scientific integrity, technical assurance, process safety or project-owner authority.

This procedure operates under the ChatGPT independent reviewer's existing, owner-ratified **REVIEWER-DECIDED** latitude.

It does not establish additional execution permissions, waive mandatory independent review, or change existing risk classifications.

## 2. Finding classes and dispositions

The four existing finding classes remain unchanged:

- **BLOCKER**
- **CORRECTION**
- **OPTIONAL**
- **RECONSIDER**

A finding requiring a change may additionally receive one of two reviewer-controlled dispositions.

### FIX AND PROCEED

Claude may implement the precisely authorised correction and continue without a separate ChatGPT recheck of that correction, provided every condition specified by ChatGPT is satisfied.

### RECHECK

Claude implements the correction and returns the affected material for independent ChatGPT verification before acceptance.

**If ChatGPT does not explicitly assign a disposition, the disposition defaults to RECHECK.**

These dispositions are not additional finding classes.

## 3. Who decides

Only ChatGPT, exercising its independent REVIEWER-DECIDED latitude, assigns FIX AND PROCEED or RECHECK.

Claude may recommend a disposition but may not assign, broaden, override or silently change ChatGPT's decision.

The project owner may explicitly override a reviewer disposition, subject to existing ratified independent-review, scientific and safety requirements.

The project owner remains the sole ratifier, execution authoriser and Git committer.

## 4. Absolute exclusion — eight always-review subjects

**OWNER DECISION, 27 October 2026: FIX AND PROCEED NEVER applies to code concerning any of the eight standing always-review subjects.**

Any change, however small, to code concerning these subjects requires **RECHECK**:

1. Process termination/kill, process ownership and the enabling switch.
2. N−1 temporal boundaries and leakage, including readers, views, digests and prefix isolation.
3. Fit seeds and canonical forecast identity.
4. TOP/WORST readout, ties and selection.
5. Holdout access and unsealing.
6. FINAL freeze, persistence and publication.
7. The synthetic-versus-real scientific result firewall.
8. Dependency upgrades, including W-23 requirements.

There are no trivial-code exceptions to this exclusion.

The requirement applies regardless of change size, apparent simplicity or whether the author believes the change is behaviour-neutral.

This restriction is binding on the reviewer as well as the author.

## 5. Where FIX AND PROCEED may be appropriate

Subject to section 4, ChatGPT may assign FIX AND PROCEED for the following kinds of changes.

### A. Non-normative documentation

Precisely specified corrections to spelling, grammar, explanatory wording, comments, counts, labels, headings or documentation where the intended meaning is unambiguous.

### B. Packaging and descriptive metadata

Precisely specified corrections that cannot alter installed content, file identities, acceptance authority, execution behaviour or safety controls.

### C. Selected trivial executable-code changes

Only where all of the following apply:

- The affected code is outside the eight always-review subjects.
- ChatGPT explicitly assigns FIX AND PROCEED to the individual finding.
- The required change is precisely specified and permits little or no implementation discretion.
- Its consequences are understood and judged low.
- It introduces no material scientific, behavioural, safety, authority or test-validity change.
- The reviewer states the permitted change, its boundaries and the required verification evidence.
- Applicable, already authorised offline tests can establish that the correction behaves as intended.

The fact that an AI can implement a change confidently is not, by itself, sufficient justification.

**FIX AND PROCEED for executable code is exceptional and case-specific, not a general entitlement.**

### D. Governing-document authority text and the Ratification Register

Only genuinely wording-level corrections that change **no rule, status or authority** may be considered for FIX AND PROCEED.

Anything affecting normative meaning, precedence, ratification status, permissions or authority requires RECHECK.

If there is uncertainty over whether a change is meaning-neutral, use RECHECK.

## 6. Required evidence for FIX AND PROCEED

Every FIX AND PROCEED finding must have a traceable finding ID and an explicit reviewer disposition.

Claude must retain:

- The exact before-and-after diff.
- The final changed-file SHA-256 identities and applicable package hashes.
- The reviewer's exact authorised correction and its scope.
- Evidence that only the specified change was made.
- The exact commands and results of applicable authorised verification tests.
- Any relevant environment and dependency versions.
- A record of what was not tested.
- Any unexpected result, discrepancy or limitation.
- The finding's REVIEWER-DECIDED identification where applicable.

Claude must also:

1. Implement only the correction authorised by ChatGPT.
2. Meet every verification condition specified by ChatGPT.
3. Identify the completed correction in the next relevant handback.
4. Provide the exact diff when ChatGPT next examines the package, including a final installation review if that is the next checkpoint.
5. Preserve the evidence for subsequent audit and handover.

A FIX AND PROCEED disposition removes the requirement for a **separate independent recheck of that exact correction**. It does not remove evidence preservation, later visibility, package verification or project-owner acceptance.

If the change requires anything beyond the authorised scope, differs materially from the agreed correction, produces a failed test, reveals another issue or cannot be sufficiently verified, it becomes **RECHECK**.

Claude must not silently expand FIX AND PROCEED to cover the additional work.

## 7. Changes ordinarily requiring RECHECK

Apart from the absolute exclusion in section 4, RECHECK is normally appropriate for changes affecting:

- Scientific or numerical formulas and algorithms.
- Statistical calibration, probability calculations or uncertainty measures.
- Test assertions, fixtures, test logic, coverage or acceptance criteria.
- Goldens, canonical identities or tie-breaking behaviour.
- Evaluators, scoring or ranking.
- Protected functions or operational safety mechanisms.
- Normative specifications or authority-bearing governing-document provisions.
- Runtime behaviour whose consequences are not unambiguously established.
- Any change for which the evidence is incomplete or unexpected differences arise.

Review depth remains proportionate to the scope of the change. RECHECK need not mean repeating the entire original review.

The distinction is **consequence and assurance, not the number of changed lines**.

## 8. Existing obligations remain unchanged

This procedure does not change:

- HIGH-tier classification rules.
- The eight standing always-review subjects.
- Required other-model independent review.
- R-1 through R-11 reviewer rights.
- The reviewer's ability to challenge designs, propose alternatives and raise RECONSIDER findings.
- N−1 isolation or holdout safeguards.
- Scientific-result and synthetic/real firewalls.
- Process termination or orphan-marker requirements.
- Owner-controlled execution, ratification, installation and Git-commit gates.

A HIGH-tier change remains HIGH regardless of whether an individual, already reviewed, narrowly specified correction receives FIX AND PROCEED.

## 9. REVIEWER-DECIDED reporting

Each disposition exercised under the reviewer's latitude must be traceable.

The existing owner instruction concerning the first three reviews under the new roles remains in force:

Claude lists every REVIEWER-DECIDED item and flags to the owner any apparent departure from ratified compliance, scientific, safety or process requirements.

That is a reporting obligation only. It does not give Claude authority to override ChatGPT's reviewer decisions or narrow reviewer rights.

## 10. Documentation and implementation

The present owner decision should be recorded accurately in the next appropriate revision of H-1 and the Ratification Register, with the existing owner review and ratification process applied to those document changes.

H-2 and the ratified roles agreement do not require immediate replacement merely to exercise this already authorised reviewer discretion.

Future reviewer handovers should reference the accepted procedure so that it is preserved across conversations.

No third AI is introduced. This procedure concerns the existing Claude-primary / ChatGPT-independent-reviewer arrangement.

It applies prospectively. Previously closed findings are not reopened or retroactively reclassified.

## 11. Guiding principle

**Use independent review where it materially improves assurance. Avoid repetitive review where a narrowly specified, low-consequence correction can be completed safely with objective evidence.**

When in doubt, choose RECHECK.

The ChatGPT independent reviewer retains responsibility for deciding which path is appropriate, within the owner's binding restrictions.

---

**End of procedural clarification.**
