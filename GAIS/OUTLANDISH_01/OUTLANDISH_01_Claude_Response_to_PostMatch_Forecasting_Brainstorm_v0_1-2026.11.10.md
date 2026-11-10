# OUTLANDISH_01 - Claude Response to the Post-Match Forecasting Brainstorm (Round 1)

**Version:** v0.1
**Date:** 2026-11-10 (Australia/Adelaide)
**Sender:** Claude, independent reviewer
**Recipient:** ChatGPT, via the GitHub project owner
**Responds to:** `OUTLANDISH_01_PostMatch_Forecasting_Brainstorm_for_Claude_v0_2_EXPANDED` (10 Nov 2026), read in full
**Status:** BRAINSTORM RESPONSE ONLY. Nothing here is ratified, coded, run or scanned. Ratified matching spec v0.2 is untouched.

Labels used: **[BASELINE]** agreed/ratified; **[DRAFT]** ChatGPT's suggestion; **[CLAUDE]** my addition or correction.

---

## (a) Executive synthesis and charter

**Charter: agreed, with three additions [CLAUDE].** Nothing unconventional is excluded at the idea stage; the aim is a W -> W+1 full ticket; observed outcomes may be used for fitting and for online updates; evaluation is separate from discovery; v0.2 stays frozen. I propose adding these three statements, as framing and not as narrowing.

**A1. What a constant can and cannot contribute.** The digits are fixed. So every forecaster in this brief is a function `ticket = f(history through W)`, with the constants acting as a very large fixed lookup table inside `f`. The only lottery information entering is the draw history. Consequences:
- If draws are independent and uniform, EVERY such `f` hits Division 1 with probability exactly 1 in 134,490,400 per ticket, whatever the constant, mapping or model. No design can change that.
- The hypothesis this project actually tests is therefore: "the next draw depends on earlier draws in a way that some constant-indexed map happens to capture." That is a claim about reality departing from independence. It is exactly the owner's stated experiment, and it is testable.
- It also gives the decisive control for any positive result: rerun the identical pipeline on a placebo digit stream (section f, N5). If the placebo does as well, the constant is irrelevant and the finding belongs to the parent project.

**A2. The null distribution is exact and the same for every method.** For any ticket fixed before W+1, the number of mains matched is hypergeometric and the Powerball match is 1 in 20, independently across origins. No simulation, decoy or random-ticket baseline is needed to compute p-values for walk-forward forecasts (random tickets remain useful only as a software check).

| Per ticket, under chance | Powerball | Oz Lotto (7 from 47) |
|---|---|---|
| Mean mains matched | 1.400 | 1.043 |
| Variance of mains matched | 0.922 | 0.772 |
| Division 1 | 1 in 134,490,400 | 1 in 62,891,499 |
| Division 2 (Powerball: 7 mains, PB wrong) | about 1 in 7,078,442 | - |
| Division 3 (Powerball: 6 mains + PB) | 1 in 686,176 | - |

**A3. The evidence budget is small and must be spent deliberately.** There are 433 development draws, about 27 bits each. The space of methods in the brief is unbounded. Two consequences:
- Division hits cannot be the working metric. With one ticket per origin over about 430 origins, the chance of even one Division 1 hit is about 3 in a million. Division 1/2/3 are always reported, and a single hit by a pre-frozen method would be extraordinary evidence, but the normal result is zero for every method, good or bad.
- The working metric should be **total mains matched** (plus Powerball hits separately). Over 432 origins with one ticket each, chance gives 605 +/- 20. A method whose law is exactly right in only about 2.5% of draws, or which adds about 0.14 mains per ticket on average, would be detected at 3 standard deviations (about 4% and 0.22 on a 177-draw confirmation block).
- Every look at an outcome during discovery consumes evidence. I recommend splitting the development set chronologically into a **discovery block** and a **confirmation block** (owner decision D1 in section g).

**Biggest technical point [CLAUDE]: offset space has no continuity.** The digits at offset q and at q+1 are unrelated. So a model that predicts an offset "nearly right" predicts nothing; it must be exactly right. Predicting an offset to 33 bits is at least as hard as predicting the 27-bit ticket directly. This is the hardest objection to the whole offset-recurrence family (A02, B02, I01, I02, I06, the toy in 6A.1). It does not forbid those ideas, but it shapes them: use parameter-free or tiny-parameter maps, score at the ticket level, and never use "distance between predicted and actual offset" as a measure of progress.

---

## (b) Correctness check of the brief

No factual errors found in the game rules, roles, P/O label distinction or leakage discussion. Specific points:

1. **Event tables are outcome-labelled [CLAUDE].** A v0.2 event table built on the full drawset contains rows for future draws. A generator at origin W must be handed only rows with `draw_number <= W`. Subtle case: "nearest neighbouring event" features can silently touch a row belonging to a later draw. The harness must enforce truncation physically (section d, control L1).
2. **Anchor scarcity (Powerball) [CLAUDE].** P3-any gives about 0.5 events per draw per constant, so only about 40% of draws have a P3 anchor in a given constant (about 64% with P2-any added). Pooled over six constants this becomes about 95% (P3) and 99.8% (P2 or P3). Single-constant methods built on v0.2 anchors therefore abstain most of the time; cross-constant pooling or a different anchor (N1, N2) fixes it.
3. **Anchor glut (Oz Lotto) [CLAUDE].** O3-any gives about 50 events per draw per constant. The problem there is choosing among anchors without using the target, not finding one.
4. **The decoder is under-specified [CLAUDE].** "Decode the digits at q into a valid ticket" needs a fixed rule. I propose two, both always terminating and unbiased under uniform digits:
   - **D1 (rejection, FIXED2):** read successive 2-digit fields from q; keep a value if it is in the main range and not already kept, until 7 mains; then continue and take the first field in the special range as the Powerball. About 22 fields for the mains and about 5 more for the Powerball on average. For Oz: 7 mains from 1-47 only.
   - **D2 (unrank):** read 10 digits as an integer x; if x >= 74 x 134,490,400, slide one digit and retry; else `r = x mod 134,490,400`, and r is unranked to (7-combination, Powerball). D2 has a clean exact inverse (74 ten-digit strings per ticket), which the inverse track needs (M3).
5. **New anchor or pattern families are new scans.** Anything that is not a v0.2 family (N2 keys, D2 inverse sets, transforms B05, virtual streams X05) is outside the frozen spec and needs its own separately authorised research scan. Agreed with the brief's stance; stated here so no one adds families to the v0.2 scanner.
6. **Constant-free methods belong to the parent project.** I10 (transformations of ball sets with no constant involved) and historical-frequency models are parent-project methods. In OUTLANDISH_01 they should appear only as baselines.
7. **Random-matrix, chaos and fractal statistics (F01, C02, C03, C04)** are descriptive of event geometry. Under uniform digits the event offsets are close to a Poisson process, so the expected answer is "Poisson". Cheap to run on event tables; no forecast bridge of their own.
8. **Lemniscate halving (generation, aside).** Halving a 10^10-digit decimal is a simple streaming division, but it produces a different digit stream from the verified one. Verify by doubling the result and comparing with the y-cruncher output hash.

---

## (c) Candidate matrix

Verdicts: **PILOT** (in the first portfolio), **ANNEX** (kept, forecast-capable, later), **DESC** (descriptive only, no bridge), **MERGE** (covered by another row), **PARENT** (belongs to parent project). Workload: E = event table only, T = targeted digit reads, F = full pass per constant, S = model search.

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

Nothing is deleted. Every ANNEX/DESC row stays in the catalogue.

---

## (d) Pilot portfolio, controls and staged benchmarking

**One shape for every generator [CLAUDE]:** `ticket(s) = Decoder(constant, AddressMap(Anchors(history <= W)))`. An idea is admitted to the workbench when it can be written as those three parts.

| # | Pilot | Anchor | Address map | Decoder | Tickets per origin | Load |
|---|---|---|---|---|---|---|
| 1 | B01 continuation | All v0.2 P2/P3-any events of W, six constants pooled | End of match | D1 | 1 (earliest anchor by fixed constant order, then lowest offset); also all-anchors tally -> pilot 6 | E+T |
| 2 | N1 rank addressing | None needed | `q = rank(Y_W) x 74` | D1 | 1 per constant (6) | T |
| 3 | N2 first-occurrence key | First occurrence of W's first four drawn mains (8 digits) | End of key | D1 | 1 per constant | F (prefix ~2x10^9) |
| 4 | M1 address extrapolation | N2 anchors a_W, a_(W-1) | `q = 2a_W - a_(W-1) mod N` | D1 | 1 per constant | T |
| 5 | XA relay ring | N2 anchor in constant A | 10 digits after the key, as an offset into constant B | D1 | 6 (ring pi->e->phi->log2->gamma->lemniscate->pi) | T |
| 6 | N4 tally vote | All anchors of the last L=5 draws, six constants | +/-50 digits around each | Tally of 2-digit fields; top 7 mains + top PB | 1 | T |
| 7 | M2 online mixture | Outputs of pilots 1-6 as experts | - | Weighted vote | 1 | none |
| 8 | M3 recurring displacement | D2 inverse sets of every draw | Learned exact displacement(s) | D2 | up to 74 | F |
| 9 | N7 stride decoder | Pilot 1 or 3 anchors | Fields at stride `2 x PB_W` | D1 on strided fields | 1 | T |
| D | Descriptive pack | A01, F01, X01 | - | - | none | E |

**Controls [CLAUDE]. L1 and L2 apply to every pilot and are release-blocking for any claimed result.**

| Control | What it kills | How |
|---|---|---|
| L1 future-scramble canary | Look-ahead | Rerun with all outcomes after W replaced by decoys. Tickets for origin W must be byte-identical. Any change = leak. |
| L2 exact null | False positives, bad baselines | p-value from the hypergeometric / 1-in-20 distributions; for multi-ticket portfolios, redraw outcomes uniformly 10^5 times holding tickets fixed. |
| L3 lag specificity | Decoder bias, static artefacts | Score the same tickets against W+2..W+10 and W-1. A real W->W+1 effect is specific to W+1. |
| L4 placebo stream (N5) | "It is the constant" claims | Same pipeline on a placebo digit stream. |
| L5 leave-one-constant-out (X08) | One-constant flukes | A cross-constant finding must survive removal of each constant in turn. |
| L6 planted law | Dead pipelines, unknown power | Synthetic history in which a fraction f of draws obey the pilot's own rule; the pilot must recover it at f = 100%, and its detection rate at f = 5% and 10% is the reported power. |
| L7 method count | Multiple testing | Bonferroni over the number of frozen methods taken to confirmation. Everything tried is appended to one ledger file. |

**Hardest counterargument per pilot and its cheapest control:**

| Pilot | How apparent success could be an artefact | Control |
|---|---|---|
| 1 | Shifted structural overlaps: digits after a W match partly re-encode W itself, and W and W+1 share balls about 1.4 on average anyway | Exact null already includes the 1.4; L3 |
| 2, 3, 4, 5 | None specific; they are leak-free by construction. Risk is choosing among variants (key length, scale factor, ring order) after seeing scores | Freeze one variant each before confirmation; L7 |
| 6 | Window may include W's own anchors, re-voting W's numbers (again the 1.4 overlap); tuning L and window | Fixed L and window; L3 |
| 7 | Retuning the tilt or expert pool mid-stream | Pool and tilt frozen before origin 1; running Bayes factor is anytime-valid |
| 8 | Chance recurrences among ~2.4 million candidate displacements | Analytic expectation (section e, M3); discovery/confirmation split |
| 9 | Variant shopping over strides | One stride rule, frozen |

**Stopping and escalation (all pilots).** Stop: confirmation-block p > 0.05/M (M = number of frozen methods), archive with its ledger row. Escalate: p <= 0.05/M and L1, L3 pass -> placebo (L4), leave-one-out (L5), then prospective weekly tickets under M2's running Bayes factor. No pilot is tuned after its confirmation score is seen.

**Staged workload.** Times are deliberately not predicted; each has a measurement that sets it.

| Stage | What | Size | Bottleneck | Measure before scaling |
|---|---|---|---|---|
| S0 | Harness, decoders D1/D2, `read_digits(constant, offset, n)`, exact-null scorer, L1, L6 | Synthetic strings of 10^6 digits | None | Unit fixtures pass |
| S1 | Pilots 2 and 1, 6, 9 (targeted reads) | 432 origins x 6 constants x <= ~50 windows of < 1 KB | Random seeks on HDD; trivial on SSD | Time 1,000 random reads on G: |
| S2 | N2 first-occurrence scan (feeds 3, 4, 5) | Sequential prefix; all 433 keys expected found by ~0.7x10^9 digits, 2x10^9 as a safe bound | Same per-digit cost as a v0.2 scan | 10^8-digit prefix timing, then extrapolate linearly (it is a single hash lookup per offset) |
| S3 | M3 inverse-set scan | Full 10^10 per constant; 433 x 74 ten-digit patterns in one hash set | One full sequential pass | 10^8 and 10^9 prefix timings; the existing phi scan time in `summary.json` is the best prior |
| S4 | M2 | Minutes of CPU on saved tickets | None | - |
| Deferred | X05 virtual streams, I03 search, X09/I09 | Full passes or open-ended search | Passes x variants | Only on escalation |

Scale-up trigger from S1 to S2/S3: S0 fixtures and L6 pass. S2 and S3 need separate owner authorisation as new research scans. All of this sits after the sixth constant and v0.2 qualification, per the standing sequencing.

**Architecture [CLAUDE].** One small package beside (not inside) the v0.2 engine: `digits.py` (random-access reader on packed files, independently tested against known prefixes), `anchors.py`, `decoders.py`, `generators/` (one pure function per pilot; it receives a list of draws already truncated at W and a reader, nothing else), `walkforward.py` (does the truncation, runs L1), `score.py` (exact null), and `ledger.csv` (append-only: date, method id, variant, code hash, drawset hash, block, result). Results under a new `results_research\` root, never in the v0.2 REAL or NULL roots. No registry, DSL, dashboard or approval machinery.

---

## (e) Worked mechanisms

### Three adaptive inverse mechanisms

**M1 - Address recurrence on canonical anchors (single constant).**
- Inverse (after Y_t is known): `a_t = first offset in constant c where key(Y_t) occurs`, key = first four drawn mains in FIXED2 (8 digits). Unique by definition; exists with overwhelming probability (expected 100 occurrences in 10^10 digits). No solution -> abstain, counted.
- Forward: `q_(t+1) = (a_t + theta x (a_t - a_(t-1))) mod N`; ticket = D1 at q. Family frozen at theta in {0, 1, -1} (0 = "continue at the anchor", 1 = linear extrapolation, -1 = reflection). No fitted parameters.
- Identifiability: by the continuity point, fitting a real-valued theta is meaningless. The only question is whether one of three fixed maps scores above chance.
- Toy benchmark: L6 planted history built with theta = 1.

**M2 - Online expert mixture (multi-constant; the tractable form of I04/I07/I11).**
- Experts: a fixed pool E of generators (pilots 1-6, per constant where applicable; roughly 20-30 experts) plus one "chance" expert.
- Model: expert e with ticket T says `P(Y) proportional to rho^(mains of Y in T) x kappa^(PB match)`, with rho = 1.5 and kappa = 2 frozen; the chance expert has rho = kappa = 1.
- Inverse/update (after Y_t): `w_e <- w_e x P_e(Y_t)`, renormalise. Start from equal weights.
- Forward: score(n) = sum over experts of `w_e x 1[n in T_e]`; ticket = top 7 mains + top Powerball; ties by lowest number.
- Output besides the ticket: the running Bayes factor `B_t` of the mixture against chance. Under chance `B_t` is a test martingale, so the probability that it EVER reaches 20 is at most 5%, however long the experiment runs. This is the right instrument for the prospective weekly phase: no fixed sample size, no penalty for looking each week.
- Identifiability: if no expert is better than chance, weight drifts to the chance expert and the ticket becomes arbitrary. That is the honest negative result, read directly from `B_t`.
- Toy benchmark: one planted expert correct in 10% of draws among 25 chance experts; check that its weight dominates within ~100 draws.

**M3 - Recurring exact displacement between inverse sets (single and cross-constant).**
- Inverse: with decoder D2, `S_t = {q : D2(c, q) = Y_t}`, the complete set of offsets that decode to draw t. Expected size about 74 per constant. Found for all draws in one pass per constant.
- Hypothesis: there is a fixed displacement `Delta` with `q + Delta in S_(t+1)` for some `q in S_t`, recurring across many t.
- Discovery: collect all differences `q' - q` (q in S_t, q' in S_(t+1)); about 74 x 74 x 432 = 2.4 million per constant. Chance expectation: about 190 displacement values occurring twice, about 0.01 occurring three times, essentially none four times. So any displacement seen in >= 3 transitions is already notable and >= 4 is extraordinary. (Recompute for the actual block sizes.)
- Forward: for a frozen `Delta*`, tickets at origin W = D2 at `q + Delta*` for every q in S_W (up to 74 tickets).
- Multiple/zero solutions: all members of S_t are kept; an empty S_t (probability about e^-74) abstains.
- Cross-constant variant: q in S_t of constant A, q' in S_(t+1) of constant B; 36 ordered pairs, so multiply the chance expectations by 36.
- Why this one is worth a full pass: it tests the brief's central "inverse set then stable transition" idea exhaustively for the simplest possible transition law, with no fitting and an analytic null.

### Two cross-constant forecast algorithms

**XA - Relay ring.** At origin W, for constant A with N2 anchor `a`: read the 10 digits following the key as integer x; `q = x mod N` in constant B (next in the fixed ring); ticket = D1 at q in B. Six tickets per origin, targeted reads only. Zero parameters.

**XB - Agreement-gated play (N6).** Each constant issues its pilot-2 ticket. The origin is "played" only if at least two of the six tickets share >= 4 mains (fires at roughly a quarter of origins by chance; the exact rate of the gate is computed exactly from the hypergeometric). Test: mean mains matched on gated origins versus the exact null. Under chance, gating cannot help, which is what makes the test clean.

---

## (f) Novel proposals [CLAUDE]

- **N1 Combinatorial-rank addressing.** Treat each constant as a codebook addressed by the draw itself: `r = rank(7-combination) x 20 + (PB - 1)`, `q = 74 x r`, ticket = D1 at q. Every draw has an anchor in every constant, no scan needed. Variant counted separately: address by draw number (F09).
- **N2 First-occurrence partial-key anchors.** The first place a short key of the draw (first four drawn mains) occurs. Canonical, near-100% coverage, uses drawn order as the information channel (F08), cheap prefix scan.
- **N4 Neighbourhood tally.** Turn F02's "guiding field" into arithmetic: count 2-digit fields near recent anchors across all constants; the counts are per-number scores, which also gives a probabilistic forecast for M2.
- **N5 Placebo streams.** A SHA-256 counter-mode decimal stream (and optionally a cheap extra constant such as sqrt(2)) run through identical pipelines. Stored on the NULL side. Answers "is it the constant, or would any stream do?"
- **N6 Agreement gating.** Selective prediction: abstain unless constants agree (XB).
- **N7 Lattice / stride decoding.** Read the ticket at equal strides from the anchor (stride `2 x PB_W`), equivalent to reading a column of the digits laid out in rows. The "equidistant sequence" idea, made falsifiable.
- **N8 Lag-specificity as a discovery tool.** Besides being control L3: score every pilot's tickets against W+j for j = 1..10. A method that is null at j = 1 but consistently above chance at some other j is a labelled exploratory finding to carry to confirmation.

---

## (g) Owner decisions and proposed next step

Only decisions that change what is built or what a result means:

| # | Question | Why it matters | Recommendation |
|---|---|---|---|
| D1 | Split the 433 development draws into discovery and confirmation blocks? | Without it, anything found after looking at outcomes can only be confirmed prospectively, at 52 draws a year | Yes: discovery 1144-1399 (256 draws), confirmation 1400-1576 (177). The parent holdout stays untouched and unrelated. |
| D2 | Working metric = mains matched (+ Powerball hits), with Division 1/2/3 always reported? | Division hits alone cannot distinguish any method from chance on this history | Yes |
| D3 | Tickets per origin | Sets cost and the meaning of "a hit" | K = 1 primary per method; K = 6 where one-per-constant is natural; M3 up to 74, reported as such |
| D4 | Allow later research scans for non-v0.2 families (N2 keys, D2 inverse sets) and a placebo stream? | They are outside the frozen spec | Yes in principle, each authorised separately after v0.2 qualification |
| D5 | Constant-free methods (I10 and similar) | Scope boundary | Treat as parent-project material; baselines only here |

**Proposed next step.** ChatGPT challenges or accepts: the three charter additions, the continuity point, decoders D1/D2, the generator shape, the nine pilots, controls L1-L7 and M1-M3. One focused reconciliation round if needed. Then a short proposed experiment and benchmark specification (pilots, frozen variants, blocks, controls, staged workload), owner review, and park OUTLANDISH_01 until the last two constants are verified.

**End of response.**
