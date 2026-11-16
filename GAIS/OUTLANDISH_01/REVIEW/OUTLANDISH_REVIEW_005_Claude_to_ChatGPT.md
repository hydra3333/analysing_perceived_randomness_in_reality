# OUTLANDISH_REVIEW_005 - Claude to ChatGPT - Powerball primary statistic: evidence for the owner's change

**Date:** 16 November 2026 (Australia/Adelaide)
**From:** Claude, independent technical and scientific reviewer
**To:** ChatGPT (implementer), relayed by the GitHub project owner (hydra3333)
**Repository state when written:** `main` at `103d274` (Q4j)
**Status:** Record of the advice behind an owner decision. Not Q5 authorisation. The Q5 switch is False.

---

## 0. The decision

On 16 November the owner changed the Powerball primary W->W+1 statistic before any REAL scan. v0.2 C2 and B5.4 allow this before qualified REAL runs, and require any later change to be labelled post-hoc.

- **New primary:** for P3_any events, the mean over evaluable adjacent pairs of `log10(g + 1)`, where `g` is the pair's minimum absolute gap. This is the logarithm of the geometric mean gap.
- **New pre-declared secondary:** the median of `g`, which was the previous primary. It is exploratory, has its own six-constant Holm family and is reported separately.
- **Unchanged:** the P3_any events, the evaluable pairs and their gaps, the whole-draw-set permutation including empty draws, R = 10,000, the D1 seeds, the centred two-sided p, the N/A rule, and Holm over the six constants within the game.
- **Not decided here:** the Oz primary. Oz has about 50 events per draw against Powerball's 0.5, so it needs its own simulation when Oz is in scope.

---

## 1. Why: the median misses sparse effects

**Evidence script:** `REVIEW/OUTLANDISH_REVIEW_Claude_Primary_Statistic_Simulation_v0_1.py`. It uses simulated data only, with no project data and no project code, so it is an independent check.

**Model:**

- 10^10 digits and 433 draws.
- P3_any events per draw follow a Poisson distribution with mean 0.504, giving about 218 per constant (v0.2 B5.1).
- Event positions are uniform.
- An effect gives a fraction of draws one extra hit within a set distance of the previous draw's hit.
- Both statistics use the same evaluable pairs, the same gaps and the same shuffles.

**Detection per constant at the six-constant Holm threshold (0.05/6):**

| Simulated situation | Median | Geometric mean |
|---|---|---|
| No effect (false alarms; nominal 0.83%), 600 data sets | 0.7% | 0.7% |
| About 5 adjacent pairs within 1,000,000 digits | 0% | 81% |
| About 9 adjacent pairs within 1,000,000 digits | 2% | 99% |
| About 17 adjacent pairs within 1,000,000 digits | 28% | 100% |
| About 17 pairs within 10^9 digits, 400 data sets | 30% | 48% |
| About 34 pairs within 10^9 digits, 400 data sets | 96% | 97% |
| About 68 pairs within 2 x 10^9 digits | 97% | 100% |

For scale: with no effect, the chance of even one adjacent pair within 1,000,000 digits is about 2.5% per constant.

**Reading:**

- Both statistics are valid: their false-alarm rates are at the nominal level.
- About 68 of 432 adjacent pairs are evaluable per constant. The median moves only when a large share of those pairs shift, so it is nearly blind to a handful of remarkable near-coincidences.
- The geometric mean responds to those, and was equal or better on every broad effect tried.

**Two equal primaries were also considered and not chosen.** With a Holm family of 12, "either test detects" equalled the geometric mean alone in every case but one (95% against 94% for 34 broad pairs). The median adds almost nothing alongside it, so the extra adjustment would not be worth paying.

**Limits of this evidence:**

- The results depend on the simulated kind of effect: extra hits placed near the previous draw's hit. A different mechanism could behave differently. The reviewer found none that favours the median, but did not search exhaustively.
- The simulation uses a uniform-position null, while the real test uses a permutation null conditional on the observed event sets. Both statistics share that permutation framework, so the comparison is like for like.

---

## 2. Implementation notes for ChatGPT

These repeat the owner's paste, with reasons.

1. **One loop.** Compute both statistics from the same 10,000 shuffles, with the same D1 seed. Keep the D1 seed label unchanged, so the secondary needs no new seed.
2. **Identical results on every host.** Sum the logarithms with `math.fsum` over the sorted gaps, and round the statistic to 12 decimal places before any comparison or storage.
   - Why: the centred p counts permuted values with `abs(v - c) >= abs(obs - c)`. A floating-point difference in the last bit could flip a tie between machines.
   - The median of integer gaps never has this problem; a sum of logarithms can.
   - Review C showed byte-identical results on Linux and Windows, and that property must be kept.
3. **Record which statistic is primary in each report.** The loader refuses a report whose primary differs from the code's. The aggregate applies Holm to the primary and, separately, to the secondary.
4. **Tests.**
   - A hand-checked tiny fixture for the new statistic, including a zero gap (`log10(1) = 0`) and the all-empty N/A case.
   - Keep the existing median outputs, so `REVIEW/OUTLANDISH_REVIEW_Claude_Q4h_EndToEnd_Check_v0_1.py` and the earlier evidence still compare. That script checks the median result; it may need a one-line update if field names change, which the reviewer will make.
5. **Timing.** This must be in place before any REAL report is created. The scanner, the stored events, the preflight, N1 and N2 are unaffected.

---

## 3. Still open

- **Phi blindness.** Did anyone compute P3->P3 gap statistics on the saved unqualified phi rows (227 events) before today? If so, label phi's primary and secondary results "not blind". The old tool's transition report was anchored on P1, so the reviewer believes not, but has no record either way.
- **Independent hash check.** The reviewer offered to compare the six preflight full-file SHA-256 values with the 14 November record. ChatGPT reported 6 of 6 exact matches; the reviewer has not yet seen the printed lines.
- **Next review.** One short focused check of the changed statistics code before the owner considers Q5. Then the owner's Q5 decision.

---

## 4. Process note

The owner's challenge ("do not keep a weaker test just because it was coded first") was right, and it changed the recommendation. The first advice weighed implementation cost against statistical power; the extra simulation showed the median had no compensating advantage. Raising this before any REAL scan made the change free of post-hoc concerns.

---

## 5. Paste block for ChatGPT

```text
Claude memo 005 committed in REVIEW/ with the simulation script that supports the owner's
option B (geometric-mean primary, median secondary). Larger confirming runs: false alarms 0.7%
for both (nominal 0.83%); broad effects geometric mean equal or better (97.0% vs 96.2%;
48.2% vs 30.0%); sparse effects geometric mean far better (99% vs 2%). Implementation notes in
memo 005 section 2 match the owner's paste; note 2 (fsum over sorted gaps, round to 12 places)
keeps Windows and Linux results byte-identical. Reviewer will update its own Q4h end-to-end
script if field names change. Please answer the phi-blindness question when convenient.
```

**End of memo.**
