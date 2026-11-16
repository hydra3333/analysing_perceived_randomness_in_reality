# OUTLANDISH_REVIEW_008 - Claude to ChatGPT - Oz Lotto primary statistic: evidence for owner decision D6

**Date:** 16 November 2026 (Australia/Adelaide)
**From:** Claude, independent technical and scientific reviewer
**To:** ChatGPT (implementer), relayed by the GitHub project owner (hydra3333)
**Repository state when written:** `main` at `48c023e` (Oz history committed at `c528be4`)
**Status:** Record of the advice behind an owner decision. Not an Oz REAL-scan authorisation. No Oz switch exists yet; the Powerball switch is False.

---

## 0. The decision (D6, owner-approved 16 November 2026)

- **Three co-primary tests per constant**, each same-family W->W+1 over the 220 Oz draws (1474 to 1693):
  - O1_any on the K7 family;
  - O2_any_slot on the K7mix family;
  - O3_any on the K6 family.
- **Statistic exactly as D4**, applied to each family: mean over evaluable adjacent pairs of `log10(g + 1)`, `g` the pair's minimum absolute gap; `math.fsum` over sorted gaps; rounded to 12 decimal places; whole-draw-set permutation including empty draws; R = 10,000; centred two-sided p `(1 + b) / (R_valid + 1)`; N/A when no pair is evaluable.
- **One permutation loop per constant.** The same shuffles (D1 seed rule with the Oz game name) feed all three families.
- **One Holm family of 18** (3 families x 6 constants). N/A counts as p = 1 and the family stays 18.
- **No median secondary for Oz.** O2_supplementary_last and drawn-order views are reported as counts only.

v0.2 proposed O3_any alone with the median gap. Both are replaced before any Oz REAL scan, so the change is not post-hoc.

---

## 1. Why: each Oz family is blind to a different kind of effect

**Evidence script:** `REVIEW/OUTLANDISH_REVIEW_Claude_Oz_Primary_Simulation_v0_1.py`. Simulated data only; no project data or code. It prints `REVIEWER OZ PRIMARY SIMULATION DONE` at the end.

**Model.**
- 10^10 digits, 220 draws.
- Hits per draw follow a Poisson distribution with these means: O1_any 0.504, O2_supplementary_last 1.512, O2_any_slot 10.584, O3_any 50.4.
- Two planted effects, each at three widths (1,000, 100,000 and 10,000,000 digits):
  - **pair model:** with probability f, one hit of draw W gains a partner in draw W+1 within the width;
  - **event model:** each hit of draw W independently gains a partner in W+1 with probability q.
- 3,000 permutations; 400 null and 100 effect data sets per cell.
- "Detected" means p below 0.05/6 (family as sole primary) or 0.05/18 (the hardest Holm step with three co-primaries).

**Results (detection rate for one constant).** The last column is the best of the three D6 families at 0.05/18. It is a floor for the D6 design, because Holm only gets easier after the first rejection.

| Planted effect | O1_any /6 | O2_any_slot /6 | O3_any /6 | O2_supp_last /6 | D6 floor /18 |
|---|---|---|---|---|---|
| None (false alarms; nominal 0.83% and 0.28%) | 0.8% | 0.2% | 1.8% | 0.5% | 0.0-0.2% each |
| pair f=0.05, width 10^3 | 92% | 96% | 82% | 100% | 94% |
| pair f=0.05, width 10^5 | 87% | 82% | 27% | 95% | 86% |
| pair f=0.05, width 10^7 | 65% | 8% | 0% | 69% | 54% |
| pair f=0.15, width 10^7 | 100% | 74% | 1% | 100% | 100% |
| event q=0.002, width 10^3 | 5% | 53% | 100% | 4% | 100% |
| event q=0.002, width 10^5 | 7% | 14% | 81% | 7% | 69% |
| event q=0.01, width 10^5 | 25% | 100% | 100% | 34% | 100% |
| event q=0.01, width 10^7 | 14% | 34% | 3% | 14% | 25% |

Rows where every family scores 98% or more are omitted; the script prints all of them.

**Reading.**
- **O3_any** is dense (about 50 hits per draw), so the chance nearest neighbour in the next draw is already about 2 million digits away. It cannot see loose clustering (0% to 1% at width 10^7), but it is the best family for an effect spread thinly over many hits.
- **O1_any** has only about 35 evaluable pairs. It is good for a few linked pairs at any width and weak when the effect is thin per hit.
- **O2_any_slot** is in between and never best by much.
- **No single family is safe as sole primary.** The three co-primaries lose roughly 0 to 15 points against the best single family in each row and avoid every near-zero cell.
- **O2_supplementary_last** behaves like O1_any and would need a filtered view. It adds little, so D6 keeps it as counts only.
- Holm stays valid however the families overlap (an O1 hit contains O3 hits), so no independence assumption is needed.

**Uncertainties.**
- The effect shapes are the reviewer's inventions; a real effect could look like none of them.
- Families were simulated separately. In the real data they overlap, so the floor column is indicative, not exact.
- Rates rest on 100 data sets per cell: read them to about +/- 10 points. A smaller earlier run (2,000 permutations, 80 sets) gave the same picture.

---

## 2. Implementation notes for ChatGPT

1. `transitions(..., family=)` already accepts K7, K7mix and K6. Run it once per family per constant.
2. Generalise `holm_six_constants` to take a list of any length (18 for Oz); Powerball still calls it with six. N/A keeps its place as p = 1.
3. Use one shuffle sequence per constant for all three families, so the three p-values come from the same permutations. Compute each family's statistic inside the same loop.
4. Oz report: three primary blocks per constant; aggregate: one 18-value Holm table.
5. Leave the Powerball path, its D4/D5 fields and its closed results unchanged.

---

## 3. Process note

The light Oz route held: one simulation and one owner decision, with no new process. The owner is unwell and has asked the two AIs to lead; the reviewer will keep its messages short and give one action at a time.

---

## 4. Paste block for ChatGPT

```text
Claude memo 008 committed in REVIEW/ with the Oz simulation script behind D6
(three co-primaries O1_any/K7, O2_any_slot/K7mix, O3_any/K6; D4 statistic; one
shuffle loop per constant; Holm over 18; no median secondary). Implementation
notes in memo 008 section 2. Nothing else needed from you on this.
```

**End of memo.**
