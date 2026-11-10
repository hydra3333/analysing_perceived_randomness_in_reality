# OUTLANDISH_01 — Post-Match, Cross-Constant, and Adaptive Forecasting Research
## Proposed experimental specification and staged benchmark plan — v0.1, FOR OWNER REVIEW

**Date:** 10 November 2026 (Australia/Adelaide)  
**Prepared by:** ChatGPT, synthesising the owner–Claude–ChatGPT brainstorming and two focused reconciliation rounds  
**Project:** `hydra3333/analysing_perceived_randomness_in_reality`, subcomponent `GAIS/OUTLANDISH_01`  
**Status:** **PROPOSAL ONLY — NOT RATIFIED, NOT CODED, NOT AUTHORISATION TO SCAN, EXPERIMENT, MODIFY DATA, OR USE THE PARENT HOLDOUT.**  
**Next step:** Owner reviews and may ratify or amend this document. Then **PARK OUTLANDISH_01 research work** until all six production constants are generated, independently verified, and published and the approved scanner qualification is complete. The owner/Claude may meanwhile return to the parent project's separately authorised major coding work. No further Claude brainstorming round is requested.

**Direct predecessors:**
- `0_outlandish_thought_experiment_01_scope.txt` (original owner objective).
- **Owner-ratified** `OUTLANDISH_01_Consolidated_Matching_Reporting_Spec_v0_2_RATIFIED.md` (the earlier document's internal header still says proposed; the owner's subsequent ratification is decisive).
- `OUTLANDISH_01_PostMatch_Forecasting_Brainstorm_for_Claude_v0_2_EXPANDED.md`.
- `OUTLANDISH_01_Claude_Response_to_PostMatch_Forecasting_Brainstorm_v0_1.md` (Claude Round 1).
- `OUTLANDISH_01_ChatGPT_Focused_Round2_Reconciliation_v0_1.md`.
- `OUTLANDISH_01_Claude_Focused_Round2_Reply_v0_1.md` (Claude's final Round 2; AGREED C01–C08, with modifications).

**Scope of this document:** Formalise the *additional* forecasting workbench, its mathematical contracts, candidate portfolio, scientific controls, and measured-runtime gates. Do **not** amend or substitute the ratified v0.2 historical matching/reporting specification. If an implementation detail below is marked **proposed binding clarification**, it is an explicit resolution for owner review, not a claim that Claude had already agreed to that exact detail.

---

# 0. SHARED CHARTER — READ FIRST; INTENDED FOR ALL THREE PARTICIPANTS

**Owner, Claude, and ChatGPT share these research principles:**

1. **Primary goal: actual next-draw prediction.** Given only information available after actual draw `W`, generate a candidate for actual draw `W+1`. Preferred Powerball target is **all seven correct main numbers in ANY order and the correct Powerball from its separate barrel** (Division 1); Division 2 and Division 3 selections are meaningful secondary targets. Oz Lotto has its own seven-main plus supplementary scoring and never mixes with Powerball. Exact prize-division scoring is separate from the v0.2 historical *pattern labels* P1/P2/P3 and O1/O2/O3.
2. **Nothing is ruled out merely for being strange.** Ordinary statistics, combinations, direct digit continuation, hidden-state inversions, cross-constant information exchange, dynamical systems, chaos, quantum-/pilot-wave-*inspired mathematics*, p-adics, fractals, spectral ideas, artificial constructions and truly wild hypotheses may be proposed. Do not suppress surprising observations simply because chance seems overwhelmingly likely. But a speculative *mathematical analogy is not a claim of demonstrated quantum or other physical causation*.
3. **Known outcomes are legitimate learning data.** Once draw `t` has occurred, its true result may be used to invert an equation, infer a hidden state, update parameters, rank models, or learn a transition rule for forecasting `t+1`. It cannot be used in the *forecast of t itself*. Retrospective discovery may inspect all approved pre-holdout historical outcomes; honest forecasting assessment requires a precise past-only chronology and transparent disclosure of model/variant selection.
4. **Fixed constants are deterministic information reservoirs.** A method may read or transform any approved constant's digits, including rescanning the entire 5-GB packed binary or combining constants. The substantive testable hypothesis is that draw history has some exploitable dependence that a constant-indexed map can capture; constant specificity requires comparison with placebo streams. Fair independent draws defeat *every* past-only forecaster, including one using constants.
5. **Use ALL approved pre-holdout data, not an internal discovery/confirmation split.** For Powerball these are exactly draws **1144–1576**, with each scored origin `W` allowed to see only draws `<= W` and target `W+1 <= 1576`. Oz Lotto uses its already-approved modern-era pre-holdout sequence and separate cutoff. The owner's decision explicitly overrides Claude's Round-1 suggestion of a 1144–1399 / 1400–1576 split. Future holdout draws and parent-project restricted outcomes remain untouched.
6. **The expected answer may be 'no relationship'.** We seek testable formulae, not post-hoc stories. Show raw effects, chance baselines, coverage, number of methods searched, negative findings and limitations. Never infer next-draw skill from matching historical outcomes after their identities are known.
7. **Compute ambitiously, but benchmark first.** Entire additional scans are allowable **in principle**, but assess `10^6`, `10^8`, `10^9`, targeted-read and other representative subsets before committing days to `10^10`. Measure actual elapsed time, CPU, RAM, disk throughput and seek costs; estimate and record scaling uncertainty. An expensive or currently infeasible idea is **deferred, not deleted**.
8. **Separate from the parent project.** OUTLANDISH_01 is an exploratory subcomponent, not automatically a supported or released predictive method. No automatic use of parent holdout, evaluation data, method registry, forecasts or coordinator. A future proposal to the parent project follows its own review, interfaces and owner authorisation.
9. **Keep the workflow simple and safe.** One well-defined candidate workbench, read-only constant files, small run identities/ledger, labelled REAL/NULL/RESEARCH outputs, independent fixtures and reproducible deterministic rules. No new rule DSL, administrative approval database, signatures or unnecessary bureaucracy.
10. **Sequence is binding.** The ratified v0.2 full-six-constants precondition remains. This is a **paper design now**. Do not begin code, scan qualification or production research merely because the owner considers this proposal. Later implementation and each large scan require explicit owner authorisation.

**Current generation note (10 Nov 2026):** `phi`, `e`, `pi`, `log2` each have a verified `10^10`-digit packed production file according to owner-reported results. `gamma` is running from a recovered y-cruncher checkpoint on the older i5, and `lemniscate` remains to be generated. Gamma/lemniscate completion or restart may take days. The possible RAM upgrade is a separate generation/recovery question; **no attempt to change y-cruncher checkpoint memory parameters is authorised by this scientific document**.

---

# 1. RESEARCH BOUNDARY, DATA AND EVALUATION TERMINOLOGY

## 1.1 Two different kinds of analysis

- **Historical match geometry (ratified v0.2):** Scan every valid decimal-digit offset for P1/P2/P3 and O1/O2/O3 outcomes; record `(draw_number, family, start_digit_offset, matched_digits)`. Classify any/drawn order, nested and shifted overlaps, expected counts, synthetic-decoy comparisons, consecutive-draw positional gap statistics, permutation tests and six-constant multiplicity. This is **not** a ticket forecaster.
- **New forecast workbench (this proposal):** At each allowed origin W, construct **complete candidate lottery tickets** using only approved history through W plus the deterministic constants. Score the ticket against draw W+1 after the prediction is fixed. It may consume the v0.2 REAL event files **with strict origin filtering** or make separately authorised additional digit scans.

**No semantic conflation:** An `O2_any_slot` or `P3_any` *digit match* is not necessarily an actual prize-winning ticket. The forecast workbench reports literal prize-selection outcomes (Division 1/2/3) for its produced tickets.

## 1.2 Input and coordinate contracts

- Six constant IDs in invariant order: `pi, e, phi, log2, gamma, lemniscate` (indices `0..5`).
- Each published constant: `N = 10,000,000,000` logical decimal digits **including integer digit**, `5,000,000,000` packed bytes, `OUTLANDISH_PACKED_BCD_HIGH_FIRST_V1`, zero-based digit offsets, even and odd starts allowed. Integer digit at offset 0. Decimal point absent. Only verified published files and receipts may serve as REAL constant inputs. `lemniscate` is the agreed *half-perimeter* representation, not untransformed y-cruncher full perimeter.
- Powerball outcome/ticket: unordered **seven distinct mains 1..35** plus independently ranged PB **1..20**. The PB may equal a main. Historical drawn order is preserved *where used as an input key*.
- Oz Lotto: unordered **seven distinct mains 1..47**; the historically drawn **three supplementary values** are used to assess Division 2 versus Division 3. Generators issue seven-main tickets only; they do not predict or select supplementary balls.
- Historical REAL datasets are the already isolated, authorised pre-holdout drawsets. Powerball development rows are exactly `1144..1576` inclusive (433 draws), giving up to **432 scored W -> W+1 origins** before method-specific warm-ups/abstentions. A forecast made from draw 1576 for target 1577 is **not scored here** because 1577 lies past the permitted cutoff. Oz draw-number boundary must come from its existing approved profile rather than be guessed.
- Each research event, key index or inverse-set index may be **precomputed once** from the pre-holdout data for efficiency, but the generator interface at origin W **must expose only past rows/keys/inverse sets** (`draw_number <= W`). Hidden future labels may not influence index statistics, tie-breaking, normalisation or parameters.
- No other variable derived from future outcomes is a legal input, including precomputed nearest-neighbour arrays, global event ranks containing future-labelled events or “best offset for W+1”. The **constant digits themselves** are accessible anywhere at an address computed past-only.

## 1.3 Categories of evidence

- **PRE-SPECIFIED RETROSPECTIVE WALK-FORWARD:** Complete candidate definitions and variants locked before any scoring of those candidates or sibling variants on real outcomes; each origin is strictly past-only. Under a genuinely independent uniform-draw null, correct single-ticket null probabilities apply. This is **not** an untouched independent confirmation set: the programme and some parameter ideas were developed with earlier aggregate historical match evidence in view.
- **EXPLORATORY / FITTED:** A model introduced or retuned after seeing its own/sibling results or searching formulas against historical outcomes. It may train or diagnose on all approved pre-holdout draws, but its in-sample historical score is **not** presented as independently confirmed prediction skill.
- **PROSPECTIVE:** Prediction fully fixed and recorded **before a genuinely later, authorised outcome is known**. Any future-outcome intake must be specifically approved without weakening the parent's untouched holdout boundary. The method must not silently bridge disallowed draws to obtain a “current” state.
- **NULL / SYNTHETIC:** Valid planted outcomes and artificial digit streams are isolated from REAL histories and results; used only for controls, power checks and algorithm qualification.

**Core statistical caveat:** Even a formula that exactly fits hundreds of historical outcomes can fail completely when forecasting the next draw. Inverse solutions must lead to a stable, past-identifiable forecast rule rather than one newly fitted parameter for each outcome.

---

# 2. COMMON GENERATOR AND HARD LEAKAGE CONTRACT

Every method has a concrete finite structure:

`Forecast_W = Decoder(constant_digit_reader, AddressMap(Anchors(history_through_W)))`

Some methods combine several constants or replace the decoder with a weighted count of candidate fields. Any such exception must still define: **past-only inputs; exact operations; finite search domain; bounded outputs; deterministic tie-breaking; abstentions; and reproducible ticket scoring**. The formula above is a useful workbench interface, **not** a restriction on future speculative brainstorming.

- **Input to pure pilot function:** immutable history prefix ending W, optional v0.2 event rows filtered to `draw<=W`, approved constant IDs/read-only digit access, frozen configuration. It never receives a later result or future-labelled inverse set.
- **Output:** zero or one **primary** valid ticket per origin, optional finite **panel** of additional distinct tickets, provenance (constant, anchor, address, decoder, parameters, trace), or `NO_TICKET` with a reason. The primary is always chosen without seeing `Y_(W+1)`.
- **Per-constant primary rotation:** For methods emitting up to six constant-specific tickets, first try constant index `draw_number(W) mod 6`, then cycle through the above six-constant order to the first valid result. If none exists, abstain. Record the full `K<=6` per-constant panel separately. A six-ticket panel does not become six independent single-ticket trials by sleight of hand.
- **Abstention:** Count every eligible origin and every no-ticket origin. Never silently exclude failures from denominator. Warm-ups with genuinely unavailable past inputs are recorded separately from eligible-but-abstained origins.
- **Invalid address:** No wrap unless explicitly stated for that method; reject negative address or reads past N; no auto-search for a better valid output. `NO_TICKET` is not an excuse to peek at a future target.
- **L1 future-scramble canary (mandatory):** For representative origins (and systematically in tests), replace *all* outcome-labelled material after W with arbitrary valid decoys, rebuild or provide those indexes, and require the forecast + trace for W to remain byte-identical. Apply to the v0.2 event table, N2 key lookup structures, and M3 inverse sets. Compare the **canonical forecast and forecast-derived trace**, not provenance fields such as the full-drawset hash that necessarily change in a scrambled test. Canary failure blocks any interpretation or release of forecasts.

---

# 3. FROZEN DECODERS AND RANK CONVENTION

## 3.1 Combinatorial rank — one convention everywhere

Use **zero-based colexicographic** combinatorial ranking for sorted seven mains `1 <= m1 < ... < m7 <= B`:

`colex_rank(mains) = sum_{i=1..7} binom(m_i - 1, i)`

where `B=35` for Powerball and `B=47` for Oz. Ranks are `0..binom(B,7)-1`. Inverse unranking returns the unique sorted seven-main combination (standard combinatorial number-system inverse); no confusion with lexicographic rank or operator-drawn order.

- `T_PB = binom(35,7)*20 = 134,490,400` possible Powerball tickets.
- `T_OZ = binom(47,7) = 62,891,499` possible Oz tickets.
- For Powerball `r = 20*colex_rank(mains) + (PB-1)`, `PB=(r mod 20)+1`, and `colex_rank = r // 20`.
- For Oz `r = colex_rank(mains)`.
- The **first four drawn mains** used by N2 are the actual historical *operator-drawn order*, not the first four of the colex sorted mains. Both representations exist for different purposes and must never be interchanged.

## 3.2 D1 — rejection decoder (used for ordinary forecast pilots)

Starting at logical offset `q`, read successive non-overlapping 2-digit decimal fields at `q, q+2, q+4, ...`, each in `00..99`. During the **mains** phase, accept only fields in `1..B` not already accepted; keep the first seven distinct accepted mains. For Powerball, then enter **PB phase**, reading subsequent fields and taking the first `1..20` as PB, allowed to equal a main. Oz stops after seven accepted mains. Return mains sorted for the ticket, independently of encountered order.

- **Total field cap:** at most **200 inspected fields across all phases combined**. If no complete valid ticket by field 200, or a required 2-digit field would extend past N, return `NO_TICKET`. No wrap, no second address, no automatic slide.
- Invalid fields and duplicate mains consume cap slots. PB may duplicate a main; there is no PB requirement for Oz.
- Under *ideal independent uniform digits*, D1 outputs uniform valid combinations conditional on producing a ticket. Its behaviour on actual mathematical-constant digits remains an empirical property, not a guaranteed random output.
- D1 implementations support an explicit **field-offset iterator**; pilot N7 supplies strided field starts but inherits this field acceptance, order, cap and EOF contract.

## 3.3 D2-core — **single-window** exact inverse decoder (M3 only)

Read **exactly 10 decimal digits** starting at q (leading zeros retained) as integer x. **Require `0 <= q`, `q+10 <= N`, and no wrap.** No sliding or retrying on rejected x.

- Powerball: accept iff `x < 9,952,289,600 = 74*T_PB`. Set `r=x mod T_PB`; unrank PB ticket. Every valid PB ticket corresponds to exactly **74** accepted 10-digit strings.
- Oz: accept iff `x < 9,999,748,341 = 159*T_OZ`. Set `r=x mod T_OZ`; unrank seven-main ticket. Every valid Oz ticket corresponds to exactly **159** accepted 10-digit strings.
- Otherwise `NO_TICKET`. Approximate rejection rates under uniform ten-digit windows: PB 0.477104%, Oz 0.00251659%.
- **Do not implement D2-retry**: a sliding/retry decoder changes the inverse-set cardinalities and is outside the agreed pilot contract.

**Verified colex/PB regression fixtures:**

| Mains | PB | Colex rank | `r` | Accepted minimum x | Accepted maximum x | `q=74*r` |
|---|---:|---:|---:|---|---|---:|
| 1 2 3 4 5 6 7 | 1 | 0 | 0 | `0000000000` | `9817799200` | 0 |
| 1 2 3 4 5 6 8 | 1 | 1 | 20 | `0000000020` | `9817799220` | 1,480 |
| 2 3 4 5 6 7 8 | 1 | 7 | 140 | `0000000140` | `9817799340` | 10,360 |
| 3 11 17 22 28 31 35 | 7 | 6,060,713 | 121,214,266 | `0121214266` | `9939013466` | 8,969,855,684 |
| 29 30 31 32 33 34 35 | 20 | 6,724,519 | 134,490,399 | `0134490399` | `9952289599` | 9,952,289,526 |

Tests additionally require x=`9952289600` rejected; Oz upper-bound x=`9999748341` rejected; exact rank/unrank round trip for every fixture; exhaustive colex bijection in a tiny `3 from 5` game; leading-zero digit reading; odd/even BCD starting offsets; EOF; and D1/PB-equals-main corner cases. The numerical fixtures and normalisers in this proposal were independently recalculated by ChatGPT, not merely copied from Claude.

---

# 4. FROZEN FIRST PORTFOLIO — NINE PILOTS, ONE OPTIONAL

**The following are research definitions intended to be frozen at owner approval, not yet implemented.** Unless expressly designated optional/deferred, all are retained even if their results appear useless. `K` is actual per-origin emitted-ticket count; `NO_TICKET` events count.

| ID | Method | Past-only source and fixed rule | Output | Work |
|---|---|---|---|---|
| **P01 B01** | Immediate continuation | For each constant, take draw W's **lowest-offset** v0.2 any-order event: PB family priority `K7S,K7,K6S` for exact tie; Oz `K7,K7mix,K6`. Apply D1 at `start + family_length`. | Rotating primary; per-constant `K<=6` panel | Event table + targeted reads |
| **P02 N1** | Colex rank address | Compute `r(Y_W)` as §3.1. PB `q=74*r`; Oz `q=159*r`. Apply D1 there in each constant. | Rotating primary; six-ticket panel | Targeted reads |
| **P03 N2** | First partial-key occurrence | Form FIXED2 **8-digit key from first four operator-drawn mains** of W. In each constant find its **earliest** occurrence inside the pre-fixed N2 prefix. D1 at `a+8`; absent key => no ticket for that constant. | Rotating primary; `K<=6` | New prefix scan |
| **P04 M1** | Linear address extrapolation | N2 anchors `a_W` and `a_(W-1)` in same constant; `q=(2*a_W-a_(W-1)) mod N`, choose representative `0..N-1`; D1 at q, requiring an available complete field window. | Rotating primary; `K<=6` | Targeted reads after N2 |
| **P05 XA** | Cross-constant relay ring | From N2 anchor `a` in source constant A, read 10 digits from `a+8` as integer `x`; target constant B is next in fixed six-constant ring; `q=x` (in `[0,N-1]`); D1 in B. | Rotating **source** constant; six-ticket panel | Cross-constant targeted reads |
| **P06 N4** | Neighbourhood tally | Use every v0.2 anchor from draws `W-4 .. W` across six constants. Sample 25 two-digit fields before and 25 after each event, with matched intervals excluded and each `(constant, field-start)` counted once. Vote mains by most occurrences (`1..B`), seven distinct; Powerball by most occurrences in `1..20`; low value breaks ties. | One tally ticket | Event table + targeted reads |
| **P07 M2** | Online expert mixture | 38 PB experts / 32 Oz experts; normalised likelihoods, online weights and vote ticket in §5. | One vote ticket, plus BF/evidence series | Saved pilot predictions |
| **P08 M3** | Exact inverse-set displacement | Use D2-core inverse sets and online recurrence selector in §6. Record **M3-3** (`R_min=3`) and **M3-2** (`R_min=2`) as distinct frozen variants. | One rotating primary; per-constant panels `K<=100` | Full 10^10 scan per constant (gated) |
| **P09 N7** | Stride decoder | PB only. Starting at N2 anchor a of W, field j begins at `a+8+2*(PB_W+1)*j` (`j=0..199`), applying D1 mains/PB logic on those strided fields. | Rotating primary; `K<=6` | Targeted reads after N2 |
| **P10 XB — OPTIONAL** | Agreement-gated play | Compare P02/N1 six tickets; gate fires iff a pair shares at least four mains. Choose pair with maximum shared mains, ties by earliest fixed constant-pair order; output earlier constant's ticket. Otherwise abstain. | One ticket when gate fires | Saved P02 outputs |

**Constant order for all rows:** `pi -> e -> phi -> log2 -> gamma -> lemniscate -> pi`. **Absence of a draw-W v0.2 match creates a legitimate P01 no-ticket**, not permission to use a match labelled with draw W+1. For P03, P04, P05 and P09, N2's key must be derived only from W or earlier draws, although the digit-search index may have been physically built offline.

## 4.1 Explicit resolutions for the implementation draft (owner review)

These are **proposed binding clarifications** to avoid ambiguous or retrospective tuning:

**N2 prefix length.** Freeze **`L_N2 = 2,000,000,000` logical digits** now as the default prospective pilot definition. It is a pre-fixed upper bound, not a prediction-performance knob. Run `10^8` / `10^9` *timing-only* trials before committing to its 2e9 scan. If the owner later changes L_N2 for operational reasons, version it **before any scores from the affected N2-derived methods are examined** and record both variants if both have been scored. Key absent within L_N2 => abstain; do **not** extend the prefix per draw until a favourable ticket appears. Prefix index may be shared by P03, P04, P05, P09.

**N4 exact field boundaries.** For event at start `s` of length L, inspect preceding full fields starting `s-2, s-4, ... s-50` (where nonnegative) and following full fields starting `s+L, s+L+2, ... s+L+48` (where they fit in N). Skip any field that overlaps **any matched interval from the same active `W-4..W` anchor set in that constant**, a conservative reading of “matched intervals excluded” that avoids counting another anchor's own digits. Deduplicate physical field starts per constant before tallying. Require all five historical draws to exist for P06's initial eligibility (warm-up of four origins); thereafter if **no usable fields remain**, return `NO_TICKET`, not an arbitrary `[1..7]` vote. Keep this globally excluded-interval detail conspicuous for owner approval because Round 2 specified exclusion but not the scope of overlaps.

**P09 stride cap.** Consume exactly the 200 possible strided field positions `j=0..199`; if an addressed two-digit field does not fit the binary, `NO_TICKET` (no wrap). The previous erroneous `2*PB_W` rule is retired; `2*(PB_W+1)` is the only candidate.

**P10 gate pair tie.** “Best pair” means maximum intersection size, ties by lexicographically lowest `(source_constant_index, other_constant_index)`, and output the lower-index source's N1 ticket. Gate decision is wholly past-only.

**M1 only linear extrapolation.** Do not retain `theta=0` or `-1` as extra M1 pilots: they decode at known current/prior keys and were correctly identified as degenerate echo strategies. Historical echo is a useful simple baseline but not the same claimed offset-recurrence mechanism.

**Eligibility:** M1 requires W and W−1; N4 requires a complete five-draw trailing window; all origin counts and exclusions are explicit. No arbitrary padding with future draws.

---

# 5. M2 — NORMALISED ADAPTIVE EXPERT MIXTURE

## 5.1 Fixed experts, parameters and vote

- **Powerball:** six constant-specific outputs each from P01, P02, P03, P04, P05 and P09 = **36 experts**, plus the one P06 tally expert and one uniform-chance expert = **38**, initial weights `1/38`.
- **Oz:** six constant-specific outputs each from P01–P05 = **30**, plus P06 and chance = **32**, initial weights `1/32`.
- P08/M3 excluded from M2 (later and potentially many tickets); optional P10 gate excluded (duplicates N1 source predictions).
- Fixed `rho=1.5` for each matching predicted main and Powerball `kappa=2` if PB agrees; Oz has no kappa. An expert at an origin with `NO_TICKET` acts as the **uniform chance expert for that origin** (likelihood ratio 1), and casts no number votes.
- The actual emitted M2 ticket is the **seven mains with highest summed current expert weights among their predicted selections**, plus highest-weight PB (PB game only); ties by lower ball number. This is distinct from the predictive probability distribution of §5.2. P02 always provides up to six legal tickets, so ordinary M2 runs have an available vote; still handle zero-vote edge case defensively as `NO_TICKET`.

## 5.2 Normalised probabilistic experts

Let `p0(Y)` be the fair-draw null over full outcomes, including PB where relevant, and `m(Y,T)` the number (0..7) of mains shared by outcome Y and expert ticket T. Under Powerball let `I_pb(Y,T)` be 1 for correct PB, 0 otherwise.

`p_e(Y | history) = p0(Y) * rho^m(Y,T_e) * kappa^I_pb(Y,T_e) / Z_PB`.

For Oz omit the kappa factor and use `Z_OZ`. For the chance or abstaining expert, set `p_e=p0`.

Exact normalisers are:

`Z_main(B) = sum_{j=0..7} [binom(7,j)*binom(B-7,7-j)/binom(B,7)] * (3/2)^j`;

`Z_PB = Z_main(35) * [19/20 + (1/20)*2] = 2.0057047468048834...`;

`Z_OZ = Z_main(47) = 1.6331472133608629...`.

Calculate combinatorial sums with stable numerical arithmetic; do not use rounded constants as the *definition*. Exact normalisation gives the expected per-origin likelihood ratio `p_e/p0` equal to 1 under the fair null, conditional on all past information.

At each origin, **write forecast tickets and distribution/evidence inputs first**, then reveal the next actual draw for scoring and update. Weight recursion is Bayesian model averaging:

`w_e(new) = w_e(old) * [p_e(Y_(W+1))/p0(Y_(W+1))] / sum_j w_j(old)*[p_j(Y_(W+1))/p0(Y_(W+1))]`.

Implement in log space. M2's vote ticket is scored by the ordinary **exact one-ticket** null; the **mixture likelihood ratio** is a separate measure of probabilistic forecasting evidence, and must not be described as the probability that the vote ticket wins.

## 5.3 Prospective Bayes factor / e-process

For a fixed mixture formulation, the per-draw predictive likelihood ratio is

`ell_W = sum_e w_(e,W) * [p_e(Y_(W+1))/p0(Y_(W+1))]`.

The product `BF_t = product_(eligible prospective origins up to t) ell_W` is a nonnegative mean-one martingale under the independent fair-draw null, provided the portfolio and update rule were frozen before the evaluated outcomes. Its `ever >= 20` event therefore has null probability **at most 0.05** for **one** pre-specified mixture, regardless of later optional stopping. It is evidence about the *distribution*, not proof of physical mechanism or a guaranteed Division 1 hit.

- Historical BF series: label **retrospective**, not a prospective 5% demonstration.
- Genuine prospective monitoring: **reset BF to 1** just before the first separately authorised genuinely future outcome; carry forward the full-history expert weights already fitted. Continue updating only after each actual outcome becomes authorised and available. This preserves the martingale property when the policy is frozen beforehand.
- The parent's reserved ten-draw holdout is **never consumed to initiate, warm, score or bridge this prospective monitor** without its own separately ratified parent-process decision. If a clean future history state cannot be constructed without crossing forbidden outcomes, postpone the prospective monitor rather than bypass the firewall.
- Multiple formally monitored mixtures need prospective multiplicity/alpha allocation; the proposed first portfolio contains just one per game, with the two games interpreted separately.

---

# 6. M3 — INVERSE SETS AND RECURRING EXACT DISPLACEMENTS

This is the most direct proposed test of the owner's “solve for hidden variables after each known draw and propagate to the next” idea. It is also the computationally expensive pilot, and **will be gated last**.

## 6.1 Build inverse sets with exactly one D2-core pass per constant

For each historical seven-main/PB outcome `Y_t` and constant `c`, define:

`S_t^c = { q : D2-core(c,q) = Y_t }`.

There are `N-9` legal starting offsets for a 10-digit window (zero-based `0..N-10` inclusive); expected count under ideal independent digits is approximately **74 Powerball** or **159 Oz** offsets per draw per constant. These are *means*, not per-draw maxima. Input scans generate a compact indexed mapping `(constant, historical_draw_id) -> sorted exact offsets` and **retain all occurrences**, including duplicates across different draw identities when applicable. No outcome after W may be exposed to M3 at forecast origin W.

- A single sequential pass of each constant is sufficient: build each 10-digit number, apply D2 threshold/rank, lookup that rank in the past-era REAL drawset's index, append all valid `(draw, q)` attributions. Read physical packed bytes once with appropriate rolling lookahead; preserve whole-file digest check, exact last valid start and odd/even offsets. This is a **new separately authorised research scan**, not a modification to v0.2 matching.
- For Powerball, at most 433 known outcomes are indexed; shared tickets may refer to several draws and must retain *all* matching IDs. Oz's modern isolated drawset is separate and Oz M3 full-size scan is deferred initially.

## 6.2 Distinct-transition recurrence selector

For historical consecutive transition `s -> s+1` and constant c, define difference set

`D_s^c = { q' - q : q in S_s^c, q' in S_(s+1)^c }`.

At forecast origin W, recurrence count

`R_W^c(Delta) = number of DISTINCT historical transitions s->s+1 with s+1<=W and Delta in D_s^c`.

Repeated pairs with the same Delta *inside one transition* contribute **one**, not multiple, to its recurrence. For any two different q values, difference `Delta` is **signed** and not reduced modulo N (no wrap in M3).

**Online selector at origin W:**
1. Candidates satisfy `R_W^c(Delta) >= R_min`.
2. Choose maximal `R_W^c`; tie by latest last supporting transition; then minimal `abs(Delta)`; final tie prefers positive Delta over negative.
3. If no candidate, `NO_TICKET` for that constant (counted). If no `S_W^c`, likewise abstain.
4. For each q in `S_W^c` ascending, consider address `q+Delta*`. Only retain if `0<=q+Delta*` and `q+Delta*+10<=N` and D2-core accepts. The **first valid decoded ticket is the per-constant primary**. The first at most `K_max=100` **distinct** decoded tickets form that constant's panel; duplicates are ignored but their provenance may be retained compactly.
5. Overall one-ticket M3 primary rotates across six constants via §2. Panels are reported **per constant**, not silently pooled into a potential 600-ticket game. Any cross-constant pooled panel would be a **separate explicit variant with a new null contract**.

**Freeze two separate same-constant variants:**
- `M3-3` / `R_min=3` **primary scientific hypothesis**. Under an ideal null, a triple-recurrence across the full history is exceptionally rare, so the expected outcome is often no tickets. That negative outcome must be retained. A triple recurrence alone is not predictive skill.
- `M3-2` / `R_min=2` is a distinct **weaker-recurrence** experiment. It may forecast often but is particularly vulnerable to chance coincidences; no retuning based on its score.
- **Cross-constant extension:** 30 ordered source/destination constant pairs (`6*5`), in addition to six same-constant cases, remain in the annex. The pair-specific exact selection/primary aggregation must be separately frozen before any forecast scores, not inferred from the best-performing pair after the fact. No 36-“cross-constant” miscount.

## 6.3 Description and inference kept apart

- Report recurrence histogram (Delta appearing in 1, 2, 3, 4+ distinct transitions), earliest/latest supporting transition, conditional coverage of possible forecasts, and exact observed offsets.
- The rough null estimate discussed with Claude is **~187 double recurrences and ~0.011 triple recurrences per constant** for 432 transitions with about 74 inverse offsets/draw. Those figures use a triangular difference distribution and average-sized sets; they are **sanity checks only**, not exact finite-sample p-values or proof of independence. Near-overlapping digit windows, repeated draw keys and varying set sizes can change the null.
- Secondary **lag-shifted discovery control**: recompute differences and recurrence histograms on `s -> s+j` for j=2..20, using the same retained inverse sets, without further binary scans. Mark as descriptive/diagnostic, not an exact exchangeable null if the chronology or overlaps break exchangeability.
- Distinguish the chance of a repeated Delta *being discovered among millions of possibilities* from the conditional chance of a subsequently fixed ticket matching the next draw. Do not apply a single-ticket p-value to the discovery search itself.
- M3 can make exact integer-offset forecasts. **Near misses in address space provide no partial credit**; evaluate the produced *ticket*. We do not assume neighbouring mathematical-constant digits are physically correlated or infer a continuous hidden coordinate.

## 6.4 Planted inverse-law synthetic test — correct the too-strong primary assertion

**Required before full-size M3 scan:** create one isolated synthetic 10^7-digit digit stream and 50 valid fake outcomes. Plant known D2-core-valid windows for selected disjoint transitions at `q_t` and `q_t+Delta_0`, separated far enough to avoid overlapping writes. In ten chosen transitions, ensure a common Delta_0 is present. An independent brute-force oracle must agree with the inverse finder on every planted ID/offset and with the distinct-transition recurrence counter (`R(Delta_0)=10` on the deliberately constructed fixture, absent extra accidental supports).

At origins prior to three *observed completed* planted supports, M3-3 should abstain **unless some other genuine recurrence is present in the synthetic data**. Thereafter the selector should choose Delta_0 if it is the uniquely best recurrence, and the generated **panel should include** the intended planted next-draw ticket where that pair exists. **Do not incorrectly demand that the first/primary ticket is always the planted winner**: a real inverse set can contain earlier q positions unrelated to the planting. A separate carefully controlled “one admissible earliest q” fixture may assert exact primary correctness. Include f=100%, 10%, 5% planted-rate/power experiments, each reproducible by recorded seed, and clearly mark them NULL.

---

# 7. CHANCE BASELINES, MULTI-TICKET CONTROLS AND EVIDENCE

## 7.1 Exact single-ticket null — no simulation required

Conditioned on any legal primary ticket fixed using only the preceding history, under independent fair draws the number of correct mains `J` follows:

`P(J=j) = binom(7,j)*binom(B-7,7-j)/binom(B,7)` for j=0..7,

where `B=35` (Powerball) or `B=47` (Oz). Powerball's separate PB-match indicator has probability `1/20` and is independent of J under that null.

- `E[J]=49/B`, i.e., **1.4 PB mains** and **49/47 ~= 1.042553 Oz mains** per primary ticket.
- For a truly pre-fixed, past-only method and the 432 PB origins (minus declared warm-ups/abstentions), primary main-hit distributions have a well-defined exact sequential null. When ticket exists at a selected origin based only on past, the conditional null for J is always the same hypergeometric; an honest score can use exact count-distribution convolution over scored origins and separately report abstention/coverage. If eligibility is adapted to earlier outcomes, explicitly condition on/report the selection process; do not treat the **observed** number of emitted tickets as an independently fixed sample size without justification. **Proposed safe aggregate fallback for any primary pilot with history-adaptive abstentions:** use a pre-fixed conditional e-process over *all* permitted chronological origins; when a legal ticket is emitted, use the exact hypergeometric conditional MGF for its J score (plus a separately specified PB component if desired), and when it abstains multiply evidence by 1. A pre-fixed positive-tilt mixture prevents choosing the best tilt retrospectively. Exact per-origin probabilities remain available regardless of abstention.
- PB prize-selection probabilities per **one fixed ticket**, exactly: Division 1 `1 / 134,490,400`; Division 2 `19 / 134,490,400` (all 7 mains, wrong PB); Division 3 `196 / 134,490,400` (six mains, correct PB). PB Division 3 event count 196 = `7*28`. These are **official selection classes**, not the P1/P2/P3 digit-match categories.
- Oz one-ticket prize-selection probabilities under independent uniform draws and three supplementaries from the remaining 40 balls: Division 1 `1 / 62,891,499`; Division 2 `21 / 62,891,499` (six mains and one supplementary); Division 3 `259 / 62,891,499` (six mains, seventh not supplementary). These formulas presume the specified modern seven-main/three-supplementary rules, and are separate from O1/O2/O3 digit matching.
- Report raw total mains, per-origin mean, PB correct count, coverage/abstention, official Division 1/2/3 counts, expected values and one-sided appropriately calibrated tails. Do **not** treat zero top-division wins as evidence that a method was necessarily useless; top divisions are overwhelmingly rare on 432 tries.

## 7.2 Per-origin panel null — exact in principle; aggregation needs care

For a **fixed panel of K distinct tickets at one origin**, let `c(n)` be the number of panel tickets containing main number n, `n=1..B`, and define total panel main-hit score `S = sum_(n in drawn main set) c(n)`. This counts all ticket-to-outcome main overlaps, **not** “best of K”, and accounts for ticket overlap.

- Conditional mean: `E[S | past panel] = 7 * mean_n[c(n)] = 49*K/B`.
- Conditional variance: `Var(S | panel) = 7 * (B-7)/(B-1) * popvar_n(c(n))` with **population** variance over all B values (`28/34` PB and `40/46` Oz). Values and normalisation are independently algebraically checked.
- **Exact one-origin probability distribution:** compute coefficients of `[u^7] product_{n=1..B} (1+u z^{c(n)}) / binom(B,7)` using a compact bounded dynamic program. The first two moments alone are **not** an exact upper-tail probability.
- Division coverage for **one fixed panel** may be counted exactly as the union of qualifying outcomes, **deduplicating overlapping tickets**. For Powerball the per-ticket *counts* are **1 Div 1 + 19 Div 2 + 196 Div 3 = 216 possible outcomes** (not the 197 mistakenly implied by combining Div 1 and Div 3 only in a Round-2 phrase). For Oz, supplementaries must be handled combinatorially; do **not** enumerate all `binom(47,7)*binom(40,3)` complete outcomes. Candidate-near-ticket main sets and exact supplementary combinatorics suffice. Div 1/2/3 of different panel tickets may overlap in outcome space; deduplicate unions.

**Additional scientific correction to Claude C06:** A per-origin panel null conditional on the available history is exact, but **naively convolving the sequence of distributions computed from the realised, history-adaptive panels is *not automatically* an exact unconditional null for the aggregate score**. Later panels depend on earlier actual outcomes, so conditioning on the entire realised panel sequence can reveal information about earlier scores. Do not label a plug-in convolution “exact p-value across all origins” without proof for that specific adaptive design.

**Proposed valid aggregate primary evidence for panels:** use a pre-fixed nonnegative **conditional e-process**. For each origin, standardise `Z_W=(S_W-mu_W)/max(1,sigma_W)` (if `sigma_W=0`, take `Z_W=0`); compute the **exact conditional moment-generating expectation** of `exp(lambda*Z_W)` from the one-origin DP; set `e_W(lambda)=exp(lambda*Z_W)/E_null[exp(lambda*Z_W)|past]`; multiply sequentially. A pre-fixed equal mixture over `lambda in {0.25,0.5,1.0}` produces another valid nonnegative e-process. The chance probability its value **ever reaches 20** is at most 5% for **one pre-specified panel statistic**, provided all panels are past-only. Use log calculations; frozen directions/λ values; correct multi-method adjustment L7. Per-origin exact tails and descriptive cumulative panel means remain informative. Other rigorously calibrated sequential methods could replace this **only after explicit pre-result approval**.

## 7.3 Methods, multiplicity, descriptive comparisons

- The scientific *primary comparison* for each pilot is **one deterministic primary ticket per eligible origin**; its chance calculation does not improve by having six constants available unless the algorithm genuinely makes a better ticket.
- Panels (`K<=6`, or M3 `K<=100` **per constant**) are explicitly separate secondary outcomes with their own chance and method-count accounting. For PB panel Powerball matching, report per-ticket PB hits and number of distinct PB values covered; handle panel prize-division coverage by exact union calculation, not `K / 134,490,400` when tickets overlap.
- **L7 method ledger** accounts for every scored ID/variant/constant, including failures/zero coverage. Simple conservative Bonferroni/Holm family accounting is available across the *pre-frozen set of primary methods*; distinguish it from the prospective e-process per game. Do not silently select the winning variant after seeing its history score and report only that one.
- Lag specificity W+2..W+10 is **diagnostic only**, because the histories/targets overlap and the method was designed for W+1. **Do not use W−1** as a placebo: it is already in model input and some models deliberately echo it.
- Descriptive random-matrix, fractal, chaos, modular and cross-constant relationships remain legitimate **even without a direct forecast bridge**. Such results belong in descriptive reports, not the scored ticket table until made into a finite past-only generator.

---

# 8. CONTROL SUITE L1–L7 AND NULL WORLDS

| Control | What it checks | Binding treatment |
|---|---|---|
| **L1 Future-scramble** | Hidden leakage from future-labelled event rows, key indexes, inverse sets, features, weights | **Release-blocking:** all frozen forecasts at origin W and traces must be identical when every outcome after W is replaced by valid decoys |
| **L2 Exact chance null** | Single-ticket hypergeometric/PB probability; correct panel conditional distribution; M2's normalisation | **Release-blocking for a claimed result:** exact one-ticket null; conditional panel DP + validated sequential aggregation; conditional/panel coverage arithmetic fixture-tested |
| **L3 Lag specificity** | Apparent W+1 effect also appears at W+2..W+10 | Diagnostic only; post-hoc lag discovery labelled exploratory |
| **L4 Placebo digits** | Is there evidence specific to named constants, versus any deterministic/random stream? | Independent reproducible SHA-256 counter-mode decimal stream with each raw byte `<250` converted to `byte % 10`, raw bytes `>=250` discarded; **materialise once** as 10^10-digit packed NULL binary with seed/digest/receipt, only if/when owner separately approves its cost. A placebo performing similarly is **not** proof of no predictability, but weakens claims about mathematical-constant specificity. |
| **L5 Leave-one-constant-out** | Does a multi-constant finding depend entirely on one lucky constant? | Rerun composite forecast with each constant withheld in turn, preserving a pre-defined missing-expert/fallback policy; calibrate multiple comparisons |
| **L6 Planted law/power** | Can code detect a known manufactured relationship, with realistic noise? | Separate synthetic histories; 100%, 10%, 5% planted adherence; track detection power, false positives and correct inverse recovered; independent oracle |
| **L7 Count all trials** | Method-shopping/multiplicity | Append each executed/frozen variation with source hash and score to one compact ledger. No deleting losers; a negative result may still be retained in future ensembles or studies. |

**Placebo stream distinction:** a fixed cryptographic counter-mode artificial stream is a control, **not** a “seventh named mathematical constant”, and never enters REAL v0.2 result directories. The proposed `byte<250` rejection gives exactly 25 byte states per digit and hence an unbiased 0..9 digit under uniform hash output assumptions; record counter layout, seed, generated length, full SHA-256 and format once before any comparison. Do not assert cryptographic independence from deterministic hashing.

**Planted-law distinction:** synthetic demonstrations show whether a proposed mechanism can be detected *when deliberately present*; they are not evidence the real lottery possesses that mechanism. Adequate planted test means known targets recovered, correct chronology, verified oracle, and no contamination of real game outputs.

---

# 9. PERFORMANCE BENCHMARKS AND OWNER-GATED COMPUTATIONAL ESCALATION

The research programme accepts that valuable ideas may take **days** if run naively. Therefore every expensive method has a smaller, scientifically meaningful timing trial. Do not extrapolate exact runtime from `10^6` alone; sample I/O as well as CPU, because these are 5-GB files and one generation machine has a relatively slow scratch HDD.

| Stage | Content | Initial data size / trials | Key measurements | Decision before expansion |
|---|---|---|---|---|
| **S0** | Pure software contracts, independent small oracle, D1/D2/colex, fabricated histories, L1/L2/L6, pilot mechanics, M3 planted law | 10^6-digit fixtures plus a **10^7-digit** inverse-law fixture; no REAL scans | correctness, peak RAM, failures, log quality, EOF/offset safety | All critical fixtures and leakage canaries PASS before any REAL method result |
| **S1** | P02 and independent P01/P06/P09 read performance; P10 gate; limited already-qualified event-table processing | Up to ~432 origins x six constants; **1,000 random seeks** per storage device; bounded windows; test one game before both | seek latency, physical read volume, CPU, event-table time, tickets/sec | Owner assesses actual targeted-I/O costs and approves larger work |
| **S2** | N2 exact 8-digit first-key prefix scan; feeds P03/P04/P05/P09 | timed 10^8-digit prefix, then timed 10^9 prefix; production contract upper prefix **2x10^9** | elapsed/10^8, hash/read, throughput, unique-key hit coverage, RAM, no duplicate start omissions | Benchmarks reported BEFORE owner authorises complete 2e9 indexing; prefix fixed for scoring |
| **S3** | D2-core inverse-set scan M3 (PB initially) | timed 10^8 and 10^9 prefixes, then **separate owner permission per full 10^10 pass** | windows/sec, total 5-GB read costs, candidate index memory, real recall vs oracle, projected full runtime | Do not embark on days of scans without evidence and explicit approval; schedule Oz variant later |
| **S4** | M2 expert walk-forward, sequential evidence, exact primary scoring, panels and summaries | Small saved ticket/output tables for 432 origins | minutes or measured CPU, accuracy and reproducibility | No empirical retuning of frozen variant based on its scored result |
| **Deferred** | Virtual/interleaved streams, prime/p-adic transformations, chaos/spectral scans, symbolic searches, 30 cross-constant inverse scans | benchmark representative prefixes or sampled windows first | project empirically; store resource upper bounds and abort conditions | Owner authorises distinct study; not silently attached to base pilot suite |

**Benchmark contract:** each trial records host/CPU/RAM/OS, storage medium and path, constant ID, source file SHA from receipt, logical prefix size, operation count, wall time, process CPU time, peak memory, bytes read and random seeks if measurable, code revision, observed throughput and projected full-run range (explicit assumptions). Do not confuse 5-GB *packed* file size with 10^10 *logical digits*. Preserve checkpoint/restart handling for **generation** separately; scanner's safe restart/partial outputs require review before any multi-day scientific run. A benchmark cannot overwrite existing REAL research reports.

**Scientific quality is a gate distinct from throughput:** a fast but mis-specified decoder is not useful; conversely an expensive but original hypothesis can remain in the annex. No policy of automatic rejection based only on the first p-value (Claude's early STOP suggestion was withdrawn). All results, including failures and negative findings, remain in the record; prioritise costly extensions by runtime, novelty, effect size and evidence quality.

**Post-six execution order:** first finish ratified v0.2 qualification Q1–Q5, and only then separately authorise S0/S1 and, if useful, S2/S3. “Six verified files” is a necessary condition, **not blanket permission to run**. The owner may authorise documentation or planning at any time without launching scans.

---

# 10. MINIMAL IMPLEMENTATION SHAPE AND OUTPUT EVIDENCE

**Proposed sibling research package, not inside the ratified matcher:**

- `digits.py`: read-only BCD random-access decoder and bounded window/field readers, SHA/receipt checks, known-prefix and odd-offset fixtures.
- `anchors.py`: past-only view of v0.2 match events; independent N2 key-prefix index; M3 inverse sets; prevents global full-data statistics leaking future labels.
- `decoders.py`: colex rank/unrank and D1/D2-core, full small-input oracle tests.
- `generators/`: one pure frozen implementation per pilot, no direct access to full outcome CSV; fixed rule hashes/IDs, explicit abstentions and candidate provenance.
- `walkforward.py`: chronological origin driver that constructs the immutable allowed prefix; freezes predictions before revealing W+1; executes L1.
- `score.py`: exact single-ticket null, prize division scorer, panel conditional DP/e-process, M2 normalisation/BF, multiplicity-aware summaries.
- `ledger.csv`: one practical append-only executed-variant record; no complex release registry or dashboards.

**Suggested distinct research output root:** `G:\OUTLANDISH_01\large_artifacts\results_research\` (or reviewed equivalent on actual research host), with separate `REAL/` and `NULL/` subtrees and new run-specific directories. This is distinct from ratified v0.2 `results/` and `results_null/`, which are not to be overwritten or conflated with new scored forecasts. No large binaries or generated null streams enter Git.

**Minimum per-origin record:** `method_id, variant_id, game, constant(s), origin_W, target_W_plus_1, eligible, abstained, reason, predicted_mains (sorted), predicted_PB_or_NA, primary/panel flag, actual_K, selected_anchor_offsets, address(es), exact decoder ID, score_after_reveal`, plus source/run IDs. Preserve leading-zero key strings, not spreadsheet-coerced numeric text. For M2 additionally record forecast weights (or stable digest plus reproducible state), conditional probability ratio, vote ticket and BF. For M3 record chosen Delta, distinct-transition support, inverse-set sizes, eligible source q count, and panel cap.

**Minimal per-run manifest:** historical drawset digest and cutoff, source packed receipt digests, constant identifiers/order, code revision/hashes, fixed pilot config and parameters, chronological span, runtime/resource summary, completed/failed status, output hashes and REAL/NULL label. Reuse existing provenance/receipt mechanisms; no new external signing process.

**Minimum aggregate report:** complete list of variants with eligibility/abstention/coverage, primary main-match total and null expectation, PB hits, Div 1/2/3 counts, panel K distribution and properly calibrated panel evidence, historical vs prospective labels, controls PASS/FAIL, estimated run cost and negative/surprising findings. Histories are not pooled between games. Distinct constant-specific reports are retained, even if a rotating primary yields just one overall forecast.

**Compact ledger columns (Claude agreed):** date, method ID, variant ID, game, constants used, code hash, drawset hash, origins eligible/scored/abstained, K, primary total mains, PB hits, Division 1/2/3 counts, null tail/evidence if valid, evidence label, notes. Extend only with run ID, exact ticket count distribution or control status when it materially resolves ambiguity; avoid an administrative “proof system”.

---

# 11. BROADER RESEARCH CATALOGUE — NOTHING DELETED

The first pilot portfolio is **not a judgement that everything else is worthless**. Preserve the full Round-1 idea catalogue and its original IDs/verdicts in the appendix below. `ANNEX` means retained for possible later finite-bridge formulation; `DESC` means currently descriptive rather than an already defined ticket generator; `MERGE` means a concrete initial representative has been selected, not that alternative versions are prohibited; `PARENT` means better placed in the parent project as a constant-free predictor or control. **None is rejected for being eccentric.**

Especially keep readily proposed future studies:

1. **Digits around matches:** targeted before/after fields, multiple displacements, full dynamic continuation, “next draw” encoded in adjacent/derived digit substrings, operator-drawn-order as information channel, and address-rule predictors learned from past outcomes.
2. **Across constants:** shared-draw matching geometry; direct relay rings and arbitrary directed constant networks; agreement/gating; joint inverse displacement sets (30 ordered distinct pairs); cross-constant digit-interleaving/virtual streams; leaving each constant out as a control.
3. **Adaptive inverse problems:** infer hidden offset/state from the newly observed draw, estimate an evolving transition map, then forecast the next state and decode its digits; Bayesian filtering, regularised recurrences, symbolic regression/MDL and online ensemble weighting.
4. **Nonlinear and highly speculative mathematics:** modular/prime/p-adic address maps, graph walks, attractor-style recurrence, information geometry, fractal/spectral analyses, quantum-chaos-inspired level-spacing statistics, pilot-wave-inspired fields and holographic/strided projections. Describe them without inventing physical evidence; require a **finite past-only map** for later ticket scoring.
5. **Different representations:** a separately versioned natural-width or combination-index encoding, offset lattices, and novel decoders. These require **new** readers/scans where applicable and must not silently change v0.2 FIXED2 definitions.

The **descriptive v0.2 W->W+1 proximity test remains in place**, as do same/shifted overlaps and decoy comparisons. This forecast research programme adds a different kind of question, not a replacement.

---

# 12. OWNER REVIEW / RATIFICATION CHECKPOINT

The two Claude–ChatGPT discussion rounds have concluded with broad agreement. **No third brainstorming round is requested.** The document nevertheless exposes four small implementation-level decisions which should be confirmed in the single owner review rather than left to a programmer's interpretation:

1. **Freeze colex + D1/D2 as §3**, nine pilots P01–P09, optional P10, the six-constant order, rotation, caps, M2 parameters, M3 `R_min` variants and L1–L7 controls. No split of the 433 approved PB historical draws.
2. **Confirm N2 `2x10^9`-digit prefix now** as the fixed production pilot key-search range (following timing-only `10^8`, `10^9` tests), or state a different immutable value before any scores are seen.
3. **Confirm N4's strict union-of-match-interval exclusion** and complete five-draw warm-up window, as a precise interpretation of Claude's self-voting correction.
4. **Confirm the sequential panel evidence method** of §7.2 and the M3 per-constant K<=100 / rotating primary arrangement. They are explicit technical resolutions of ambiguities; the single-origin null math itself is agreed.

**Proposed owner decision:** Ratify this v0.1 with any recorded corrections as the **future experimental specification**, with implementation **ON HOLD** pending: (i) six completed, independently verified published constants; (ii) finished v0.2 Q1–Q5 qualification; (iii) fresh explicit owner go-ahead for the relevant S-stage and any large scan. All parent predictive-randomness holdout and governance restrictions remain independently binding.

**After ratification:** Archive the proposal, preserve the Round-1/Round-2 exchange files as historical context, do not start OUTLANDISH code or computational tests, and return Claude to the already-authorised major parent-project design/coding workflow. When generation completes, reopen the approved v0.2 qualification and *then* the benchmarked forecasting pilots.

---

# APPENDIX A — Round-1 candidate catalogue, retained verbatim in substance

The following is a **reference catalogue of brainstorming dispositions** from Claude's Round-1 reply; it does **not** by itself freeze any additional candidate's parameters or authorise any implementation. The first portfolio is defined solely in §§3–6 above.

| ID | Verdict | Bridge / comment | Load |
|---|---|---|---|
| A01 gaps, clusters | DESC | Expect Poisson; run once as a health check of event tables | E |
| A02 draw-lag families | ANNEX | Bridge only via exact offset maps; see continuity point | E |
| A03 category transitions | DESC | Mostly structural overlaps; low value | E |
| A04 multi-match per draw | MERGE | Into B03 / N4 (pooling of anchors) | E |
| A05 ranks, order statistics | DESC | No exact bridge | E |
| A06 modular geometry | ANNEX | Large multiplicity; only with a pre-fixed modulus list | E |
| A07 marked point process | DESC | Formal version of A01/A03 | E |
| A08 motif mining | DESC | High overfit risk at ~3 events per draw | E |
| A09 value-feature relations | DESC | Conditioning artefacts dominate | E |
| B01 immediate continuation | **PILOT 1** | Decode D1 right after each anchor of W | E+T |
| B02 displacement continuation | ANNEX | After B01; fixed displacements only | T |
| B03 consensus voting | MERGE | Into N4 (tally) | T |
| B04 context fingerprints | ANNEX | Features >> data; only inside M2 as experts | T |
| B05 re-encodings | ANNEX | Each is a new decoder; one (N7) piloted | T/F |
| B06 pointer chains | MERGE | Into XA relay | T |
| B07 long-scale context | DESC | No bridge | F |
| C01 predictive information | MERGE | M2's log score IS the predictive-information estimate | - |
| C02 recurrence dynamics | DESC | See b7 | E |
| C03 fractal structure | DESC | See b7 | E |
| C04 phase locking | DESC | See b7 | E |
| C05 graphs | DESC | No bridge beyond what N4 already uses | E |
| X01 shared draw identities | DESC | Needed anyway for anchor coverage (b2) | E |
| X02 cross-constant geometry | ANNEX | Exactness problem; 30 ordered pairs of multiplicity | E |
| X03 location handoff | **PILOT 5** | As XA relay ring | T |
| X04 multi-constant ensemble | **PILOT 6** | As N4 tally and N6 gating | T |
| X05 virtual streams | ANNEX | Under uniform digits just another stream; do only after a single-constant signal | F |
| X06 synchronisation | DESC | No bridge | F |
| X07 offset graph walks | MERGE | Into XA | T |
| X08 invariance across constants | **CONTROL** | Leave-one-constant-out replication of any finding | - |
| X09 coupled dynamics | ANNEX | Needs a concrete finite algorithm first | S |
| F01 level spacing | DESC | Cheap; expect Poisson | E |
| F02 guiding field | MERGE | N4 is the concrete version | T |
| F03 strange-attractor maps | ANNEX | Ball-space maps -> PARENT; offset-space maps -> continuity problem | S |
| F04 prime / p-adic | ANNEX | Only as pre-fixed address functions | T |
| F05 renormalisation | DESC | No bridge | F |
| F06 holographic projection | MERGE | N7 (lattice/stride) is the concrete version | T |
| F07 compression | MERGE | Into M2 (log score = code length) | - |
| F08 operator order as channel | ANNEX | Used inside N2 (drawn-order key) | T |
| F09 date/index synchronisation | ANNEX | Draw number as address is legal (known at W); one variant in N1 | T |
| F10 Claude additions | see (f) | N1-N7 | - |
| I01 regularised inverse | MERGE | M3 is the exact, regulariser-free version | F |
| I02 affine/modular recurrence | **PILOT 4** | As M1, parameter-free members only | T |
| I03 symbolic regression | ANNEX | Search budget >> evidence; only inside discovery block, max one frozen formula out | S |
| I04 Bayesian filtering | MERGE | M2 is the tractable form | - |
| I05 multi-offset ensembles | MERGE | N4 | T |
| I06 cross-constant inverse handoff | MERGE | XA (forward) and M3 cross-constant (inverse) | T/F |
| I07 online model weighting | **PILOT 7** | As M2 | - |
| I08 chaos latent maps | ANNEX | See F03 | S |
| I09 quantum-inspired maps | ANNEX | Needs a finite algorithm; compare with plain algebraic twin | S |
| I10 ball-space inverse | PARENT | No constant involved | - |
| I11 MDL | MERGE | M2 | - |
| I12 extreme variants | ANNEX | Admit when written as (anchor rule, address map, decoder) | - |

**End — OUTLANDISH_01 proposed post-match adaptive forecasting specification v0.1, for owner review.**
