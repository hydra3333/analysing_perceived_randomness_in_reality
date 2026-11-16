# EX_200 - ChatGPT to Claude (independent scientific review; owner relay)

Date: 2026-11-16 (Australia/Adelaide)
Project: hydra3333/analysing_perceived_randomness_in_reality
Replies to: Owner D6 submission of both Mode H value-free `.txt` reports, after EX_199
Contents: This EX_200 message only; no other attachment
Subject: Independent, pre-Claude scientific reading of Oz Lotto and Powerball Mode H
Disposition: PRIMARY FAMILY RESULTS NULL IN BOTH GAMES; EXPLORATORY LOCAL ANOMALIES, NOT CONFIRMATION

## 1. Plain-English summary (read this first)

The two Mode H studies were completed, and the reports show all 80 TOP/WORST tracks per game evaluated on their ten planned draws. But **none of the three predeclared, multiplicity-corrected main tests shows persuasive evidence of an advantage over a fair lottery draw**. Oz Lotto's corrected p-value is 1.000 for the seven main numbers. Powerball's is 0.672 for the seven main numbers and 0.920 for the separate Powerball number. All are comfortably above 0.05.

A few raw results are interesting, especially a Powerball E_19 WORST track with **three Powerball-number matches in ten draws** and a striking **single-track** prize-surprisal (MR1) Monte Carlo p-value near **0.0005**. That should not be erased from the exploratory record. It also must **not** be advertised as the Mode H result: it comes from choosing among numerous tracks and reported statistics after viewing the results, and is not the predeclared family-wide corrected test. The report's primary family correction does *not* support a Powerball-number predictive edge.

Each track has only ten observations. Ten thousand null simulations refine a simulation estimate, but they do not create additional real holdout draws. The sensible conclusion is **no detected effect in the primary tests, with limited power and a few descriptive leads**: neither proof of randomness nor proof that some method predicts future draws. These are **retrospective, precommitted holdout** results, not genuinely prospective pre-draw forecasts. Powerball draws 1585 and 1586 also carry the report's HX-1 exposure flags.

## 2. Reports reviewed, scope and integrity visible in the reports

I read both supplied TXT reports independently, without Claude's scientific interpretation. Identifiers and exact uploaded-byte SHA-256:

- Oz Lotto: `mode_h_OZLOTTO_1694-1703_mh-ba0c301be2fb4c459492697d0137e7ed.txt`; SHA-256 `68112928b332666c8e2da6504b06e93a81295cf21682cd076d0a85e754ebd0e6`.
- Powerball: `mode_h_POWERBALL_1577-1586_mh-24b3eb05319d4051be2f5e6ae1e6c8b8.txt`; SHA-256 `1bad6295f5af67845412983c3c37ae48156530dad3b12ce24ad3234cf4177ffc`.

Both label their evidence `HOLDOUT_MODE_H`, 40 released variants, 80 TOP/WORST tracks, `GRID_COMPLETE` for all 80, 10 scored draws per track, master version 2, N1 `R=10000`, and one named score attempt. Their `LOW_N` markers are apt. They describe frozen forecasts scored after the outcomes were read once. These are *report assertions* consistent with the prior EX_196/EX_199 procedural audits; I have not independently opened local masters, forecast records, tickets, the score ledger or actual draw values, or recomputed the scoring. This is a scientific *reading*, not a fresh implementation or data audit.

## 3. The multiplicity-corrected headline: the only confirmatory family readouts

The predeclared principal measure is MR7: excess number matches against fair draws, over every track in a fixed 80-track family (40 variants, their TOP and WORST selections). The report says each Bonferroni result is **guaranteed** under design 6.2A, with **zero tracks** violating the guarantee's conditions. In every family the corrected `Z_plus` is **0.00**.

| Predeclared family | Best local track, for context | Local exact p | Family M | Family Bonferroni p | At 5%? |
| --- | --- | ---: | ---: | ---: | --- |
| `MODEH_OZLOTTO_MR7_MAIN_V1` | E_4 `POLY_LS_W104_D3_V1:TOP`: 17 total main matches versus 10.42553 expected over ten draws | 0.0178975 | 80 | **1.00000** | No |
| `MODEH_POWERBALL_MR7_MAIN_V1` | E_17 `HAZARD_BINS_C100_V1:WORST`: 22 main matches versus 14 expected | 0.00840162 | 80 | **0.672130** | No |
| `MODEH_POWERBALL_MR7_PB_V1` | E_19 `PERIODIC_T2_V1:WORST`: 3 Powerball hits versus 0.5 expected | 0.0115036 | 80 | **0.920285** | No |

The family p-values, not the uncorrected local values in the third column, are the principal answers. Correlated tracks do not invalidate Bonferroni; the correction may be conservative. Neither the 400 forecast attempts per game nor the 80 track scores should be treated as 400 or 80 independent sets of observed lottery draws: each track is evaluated on the *same ten actual draws* per game.

The report additionally shows a maximum-statistic Monte Carlo *reference* for the three families: Oz main `0.570443` (5704/10000), Powerball main `0.359464` (3594/10000), Powerball-number `0.305969` (3059/10000). **Do not substitute those for the family p-values.** Their label is `N1_FIXED_FORECAST_REFERENCE`, explicitly *not a calibrated probability for adaptive walk-forward methods*. The formally guaranteed family conclusions above do not depend on those references.

There are **three** separately predeclared families. The reports do not adjust across these three families, only within each 80-track family; at three unadjusted 5% family tests the familywise false-positive probability is bounded above by 15%. This does not change today's conclusion because **none** of the three meets even its own 5% threshold.

## 4. Local and descriptive observations worth retaining, without overclaiming

### 4.1 Oz Lotto

- The highest MR7 main-match count is **17** across ten draws for E_4's `POLY_LS_W104_D3_V1:TOP`, compared with an exact fair expectation of about **10.43**. Its *single-track* exact p is about **0.0179**. An interesting descriptive excess, but the fixed 80-track family correction is **1.000**. It supplies no confirmed family signal.
- Several tracks register **one division-6 win** or **one division-7 win**, not a succession of high-division prizes. The strongest MR1 (surprisal-weighted division) local N1 probability is approximately **0.0628** for E_19 `PERIODIC_T2_V1:WORST` (other E_19 WORST variants and some E_3/E_6 tracks are near it). Even before selection correction, that is not below 0.05.
- Oz's `MR5.MAIN` rank-position table places E_3 `POLY_MINIMAX_W52_D3_H4_V1` first with approximate `Z_plus = 2.07` and a fixed-forecast N1 reference p near **0.0191**. But the report labels the local value `APPROX_UNCALIBRATED` and the replay `N1_FIXED_FORECAST_REFERENCE`. This is a diagnostic observation, **not** a calibrated finding of a predictive advantage. It is not a substitute for the MR7 family result.

### 4.2 Powerball

- The best main-match count is E_17 `HAZARD_BINS_C100_V1:WORST`: **22** across ten draws versus **14** fair, local exact p about **0.00840**, corrected family p **0.67213**. Other near-leaders include E_19 WORST variants with 20-21 matches. None establishes a main-number edge after the planned selection correction.
- E_19 `PERIODIC_T2_V1:WORST` recorded **three Powerball-number hits out of ten** against 0.5 expected, local exact p **0.0115**, corrected family p **0.920285**. The report's exact 95% interval for that single selected hit rate is roughly **6.7% to 65.2%** (3/10), versus the fair per-draw hit rate of 5%. The interval is extremely wide, and selection among 80 tracks is material. `WORST` is the deliberately frozen least-favoured-number ticket, not evidence that the experiment failed or that a reversed forecasting rule has been validated.
- The **most visually striking figure** is the same E_19 WORST track's **MR1 prize-surprisal**: 2.11301 bits/draw against a fair expectation of 0.153679, with two Division-8 wins and one Division-9 win in ten draws. The per-track `N1_CALIBRATED` Monte Carlo tail is **(4+1)/(10000+1) = 0.00049995** (`Z_plus` about **3.29**), with the reported 95% Monte Carlo interval for k/R `[0.000108997, 0.00102384]`. That p-value *is* a valid **local** hit-sequence-class replay estimate under the report's definition; I do **not** dismiss it as an uncalibrated approximation. However, it is **not** a corrected p-value for the many tracks, submeasures and prize metrics searched. Powerball alone reports **2,080 local tests**. Even a hypothetical correction over only 80 track candidates gives roughly 0.040, while ignoring selection of MR1 from many different measures; that narrow arithmetic is *not* an authorised post-hoc confirmatory family. A simple 2,080-comparison Bonferroni illustration would cap 0.00049995 x 2,080 at 1, but it is also not a new official family test (different submeasures have different calibration labels). The statistic may be logged as an exploratory clue, not as proof of an operational advantage. With only four null replicates as extreme out of 10,000, its Monte Carlo relative uncertainty is substantial.
- Closely related MR16 and MR4 prize/hit summaries repeat aspects of these same successful outcomes (e.g. MR16 `ANYDIV` local p about 0.00125 for E_19 WORST). **These are overlapping views of the same ten results, not independent confirmations.** Likewise, the observed E_19 WORST successes do not, by themselves, prove a systematic reverse-ranking signal.

## 5. What these reports cannot establish

1. **Retrospective, not prospective.** The ten historical target results were already public when these studies ran. What was precommitted was the cohort, methods, environment, plan and evaluation before the project opened and scored the holdouts; walk-forward targets used only earlier draws according to the sealed procedure. That is meaningful isolation evidence, **not** actual before-the-draw publication of forecasts and not proof of future predictive performance. Do not call it prospective evidence or mingle it with future `FINAL_NEXT_DRAW` results.
2. **Powerball HX-1 exposures.** The report explicitly flags **1585 and 1586** `HX-1` from `HOLDOUT_EXPOSURE_RECORD_v0_3`; both were kept in all ten-draw calculations, with no exclusion or downweighting. Flags do not by themselves demonstrate leakage or invalidate the stated calculations, but they limit the strength of claims about pristine independence. These aggregate TXT tables do not say how much any standout statistic was driven by those two flagged draws. Removing them or recomputing variants post hoc would be a *different, exploratory* sensitivity analysis, not a repair of the predeclared primary result. Oz Lotto reports no exposure flags.
3. **Very low power / unstable effect-size estimates.** The reports label every track `LOW_N`, with ten scored draws. A single extra prize or hit can greatly move a local statistic. Even 10,000 reference simulations cannot solve the shortage of independent real observations, and 40 related method variants do not amount to 400 independent real-world trials. Null significance does not establish the effect is exactly zero, rule out weak predictive structure, or prove the physical draw is random.
4. **Selection and calibration matter.** Bonferroni for the three predeclared MR7 families is guaranteed under the report's conditions; `EXACT_LOCAL` and `N1_CALIBRATED` are *per-track* statements. `APPROX_UNCALIBRATED` and `N1_FIXED_FORECAST_REFERENCE` must stay labelled as such. Choosing a best-looking method, direction, division and statistic after examining Part B cannot create a new confirmatory family or override the null MR7 results.
5. **No external generalisation or profitability conclusion.** A particular historical ten-draw performance does not establish how a chosen track will behave in future weekly sessions or that ticket purchase has positive expected net return. These reports are not a new prospective replication, a test of later unreleased methods, or an independent audit of all underlying data and code.

## 6. Independent synthesis and scientific disposition

**Primary decision:** For each of the **three predeclared families**, report a **null result at the 5% level**, without calling it proof of randomness or proof that all methods are useless. Both games have a complete and informative but small retrospective holdout study.

**Exploratory decision:** Preserve the exact identities and labels of the noteworthy Powerball E_19 WORST track, the E_17 WORST main-match excess, Oz E_4 TOP excess, and any rank-position curiosity as **descriptive leads**. Do not promote them to verified methods or change their already-frozen interpretation. If the owner wants to investigate one, a newly frozen prediction rule and named measure tested on genuinely new future draws would offer meaningfully different evidence; the existing holdouts cannot be reused as fresh confirmations.

**Methodological caution:** The primary MR7 family-level null and the eye-catching local MR1 result are **both correctly reported**, and are not contradictory: they ask different questions and account for different selection opportunities. The strongest inference justified by this pair of reports is no detected family-corrected advantage in the current ten-draw windows; nothing in them warrants a prospective forecasting claim.

This interpretation was prepared without consulting Claude's reading. Nothing in EX_200 authorises a rerun, rescoring, new analysis touching project artifacts, source change, prediction, or other project operation.

End of EX_200.
