# Predictive Randomness - E_6 specification (lead method) and the new-method template, design note v0.1

**Document:** the method-level specification of E_6's first variants (R2 v0.5 section 7.1: "formula/details still subject to R2 method-level approval"), the design of the package that adds them, and the design of the reusable template for later methods.
**Version:** v0.1 DRAFT for the reviewer's design-stage review (R-3), 30 October 2026. Author: Claude. Ratifier: the project owner.
**Status:**
- **Authority:** it authorises no installation, run, data access, switch or allowlist change. It changes no ratified rule; E2R-1 v0.3r3 (`0a73c92d...a954`) and the CODE-1/CODE-2 libraries are used as installed.
- **Speculative code:** at the owner's request (29 October 2026, "go as far as you can"), Claude has also written the candidate this note describes (section 9). As agreed for CODE-2, it is for review only after this design passes unchanged.
- **Base:** commit `f9de54a` on `main` (CODE-2 at `ced9b6c`; handovers and register v0.14 at `337b5b2`).
- **Owner's plan (29-30 October 2026):** E_6 first, as the lead method and the template's first real use; then E_3 and E_4 with a shared Chebyshev fitting helper; then the E_7-E_16 frequency family made from the template.

## 1. In plain English

**E_6 asks:** if each number has its own steady chance of being drawn, what does the history say that chance is now?
- For each number separately, E_6 treats every past draw as a yes/no trial: was this number drawn or not?
- It estimates the number's chance from that record, using the standard Beta-Bernoulli model. That model starts from a small, fair-draw prior and updates it with the evidence.
- **Forgetting:** in the forgetting variants, older draws count for less. Each draw back counts a fixed fraction of the one after it.
- Each number's estimated chance is its score. TOP is the 7 highest (1 for the Powerball), WORST the 7 lowest, as for E_1.
- The chances are also published as probabilities, clearly labelled as model outputs, not calibrated forecasts ("mark, never suppress").

**Why it is a good first method:**
- It is simple, deterministic (no random seeds), cheap, and fully exact (section 2.4).
- With no forgetting it must rank the numbers exactly as E_1's counts do, so the frozen E_1 checks it (section 6.1).
- Its shape is the shape most later methods share: per-number scores, settings fixed per variant, and probability outputs. That makes it the right base for the template.

## 2. The specification (E_6, revision 1)

### 2.1 What is modelled (R2 7.1: "target random variable")

For game G, barrel B (MAIN, or POWERBALL for Powerball), label j, and each eligible draw d before the target N:
- x(d, j) = 1 if j was drawn in barrel B at draw d, else 0. For the Powerball barrel at most one label has x = 1 per draw.
- E_6 models x(d, j) for each j separately as Bernoulli trials with an unknown inclusion rate theta_j. This is the per-number fitted distribution of R1/R2 E_6.
- **Order of the main numbers and dates are not used** (view `UNORDERED_SET`; `uses_dates` false).

### 2.2 The rule (R2 7.1: "distribution family, sparse-data treatment and normalisation")

- **Family:** Beta-Bernoulli. A Beta(alpha_B, beta_B) prior on theta_j, the same for every label of the barrel.
- **Sparse-data treatment (the prior):** the prior is centred on the fair-draw inclusion rate and is worth exactly one draw.
  - The fair-draw rate is r_B = s_B / L_B, where s_B labels are selected from L_B in each draw: 7/35 for Powerball MAIN, 1/20 for the Powerball, and 7/47 for Oz Lotto MAIN.
  - So alpha_B = r_B and beta_B = 1 - r_B, and alpha_B + beta_B = 1.
- **Forgetting:** a draw that is a draws older than the newest eligible draw (N - 1) has weight w(a) = lambda^a, so the newest has weight 1. lambda = 1 means no forgetting.
- **The weighted evidence:** k_j = the sum over d of w(N - 1 - d) * x(d, j), and W = the sum over d of w(N - 1 - d).
- **The estimate:** the posterior mean, p_j = (alpha_B + k_j) / (1 + W).
- **Normalisation, exact by construction:** the sum over j of k_j equals s_B * W, because each draw selects s_B labels. So the sum over j of p_j is (L_B * r_B + s_B * W) / (1 + W), which is exactly s_B: 7 for MAIN, 1 for the Powerball. No renormalisation is done or needed.
- **The forgetting factor itself is never decayed** into the prior: the prior always weighs one draw.

### 2.3 Outputs (E2R-1 sections 5 and 7)

**Per barrel channel:**
- `ranking_kind` `RANKING_WITH_SCORES`, `score_type` `FLOAT64`, with the scores equal to p_j;
- TOP `TOP_MARGINAL`, WORST `INVERSE`, `readout_selection_rule_version` `TOP_MARGINAL_AND_INVERSE_V1` (as E_1);
- ties by `TIE_SHA256_V1`, which the contract applies.

**Probabilities:**
- MAIN `MARGINAL_INCLUSION_PROBABILITY` (sums to 7) and Powerball `PB_CATEGORICAL` (sums to 1), with the vector equal to the scores;
- tolerance 1e-12;
- `smoothing_note`: "Beta prior centred on the fair-draw inclusion rate and worth one draw.";
- `calibration_note`: "Posterior means of independent per-number Beta-Bernoulli models. Not calibrated: the model ignores that the 7 main numbers are drawn together, and no calibration has been tested.".

**Other declaration fields:**
- `minimum_history_draws` 1 (as E_1);
- no diagnostic record;
- `is_capability` `IS_NOT_APPLICABLE`;
- deterministic (`stochastic_fit` false, no seed policy);
- `fit_sampling_model_version` `BETA_BERNOULLI_POSTERIOR_MEAN_V1`;
- for Oz Lotto, the MAIN channel only.

**Justification for publishing probabilities** (R2 7.1: "probabilities only if justified"): p_j is the exact posterior predictive inclusion probability under the stated model. The model is simple and its weakness is named in the calibration note. Publishing the numbers with that label suppresses nothing and claims nothing.

### 2.4 Exact arithmetic (cross-platform identity)

All arithmetic is done with Python's exact fractions (`fractions.Fraction`):
- lambda is a ratio of small integers;
- every weight lambda^a, every k_j, W and p_j is an exact rational;
- each p_j becomes a float64 once, by `float(Fraction)`, which is correctly rounded and the same on every platform.

There is no `pow`, `exp` or `log` on floats anywhere, so Windows and Linux give byte-identical records. Cost: about 433 x 35 exact multiply-adds per target, a few milliseconds.

### 2.5 The variants (fixed in revision 1; owner decision D6-2)

| `variant_id` | lambda | Half-life (draws, about) | Meaning |
|---|---|---|---|
| `BETA_BERNOULLI_FULL_MEMORY_V1` | 1 | none | every past draw counts equally |
| `BETA_BERNOULLI_DECAY_74_75_V1` | 74/75 | 51.6 (about a year of weekly draws) | recent year matters most |
| `BETA_BERNOULLI_DECAY_149_150_V1` | 149/150 | 103.6 (about two years) | slower forgetting |

- Half-life = ln 2 / ln(1/lambda); shown for explanation only, never computed by the method.
- **All three are in revision 1's code from the start.** By E2R-R14A, adding a value later would be a code change and a new revision, so the set is chosen now.
- **Both games:** each variant is declared for Powerball and for Oz Lotto, so 6 declarations. Oz Lotto contract runs stay synthetic only, like everything else.

### 2.6 Worked example (the hand-checkable fixture)

Powerball MAIN (r = 1/5), target N with two eligible draws, the newest at N - 1.

| Label was drawn in | `FULL_MEMORY` (W = 2) | `DECAY_74_75` (W = 149/75) |
|---|---|---|
| both draws | (1/5 + 2) / 3 = 11/15 | (1/5 + 149/75) / (224/75) = 41/56 |
| the newest only | (1/5 + 1) / 3 = 2/5 | 90/224 = 45/112 |
| the older only | 2/5 | 89/224 |
| neither | 1/15 | 15/224 |

**Sum check:** take two draws with no number in common, so 7 labels are newest-only, 7 older-only and 21 in neither:
- **No forgetting:** 14 x 2/5 + 21 x 1/15 = 7.
- **Decay:** 7 x 90/224 + 7 x 89/224 + 21 x 15/224 = 1568/224 = 7.

The tests check these exact values.

### 2.7 Relation to other methods (honest overlap)

- **E_1:** with lambda = 1, p_j is an increasing function of E_1's count. So E_6 `FULL_MEMORY` has exactly E_1's equal-score groups in E_1's order (section 6.1).
  - Its TOP and WORST can differ from E_1's only where equal counts straddle the 7th place, because the tie rule includes the method and variant IDs.
  - Its registry text says plainly that it ranks like E_1.
- **E_7 (Bayesian frequency shrinkage) and E_9 (exponentially decayed rates):** they look at the same "weighted recent frequency" information (an overlap noted on 26 October 2026). The decay variants will rank much like E_9 would.
  - E_6 is kept distinct by its R1/R2 definition: one fitted distribution per number. Later E_6 variants can add per-number waiting-time and hazard fits (geometric, discrete survival).
  - E_7's difference is pooled shrinkage with a fitted concentration.
  - The project's rule applies: overlap is reported (rank correlation), never a reason to exclude.

## 3. What the package adds and changes

**New files:**
- `src/methods/E_006/__init__.py`;
- `src/methods/E_006/beta_bernoulli.py` (the mathematics only: the variant table and the exact posterior; it imports nothing from the project);
- `src/methods/E_006/contract.py` (`compute(task, view)` and `verify(task, view, forecast, diagnostic)` for the shared runner);
- `src/methods/E_006/IN_DEVELOPMENT.txt`;
- `src/methods/_common/contract_data/declarations/{POWERBALL,OZLOTTO}/E_6/<variant>/r1.json` (6);
- `src/methods/_common/contract_data/registry/{POWERBALL,OZLOTTO}/E_6/<variant>/entry_0001.json` (6), each `FORMULA_OPEN` with its declaration;
- `tests/test_e6_beta_bernoulli.py`;
- the template under `doc/METHOD_TEMPLATE/` (section 7);
- this note under `doc/`.

**Replaced files (whole-file, listed and checked):**
- `src/methods/Method_Contract_Runner.py`: one import and one `ADAPTERS` line, `'E_6': E_006.contract`.
- `tests/test_e2r_contract.py`: one line. The CRLF registry test asserts exactly 124 chains, the installed count. It now asserts the number of chain folders actually installed, so adding a method's chains no longer means editing it.
- `tests/test_e2r_dispatch.py`: one guard. CODE-2's static guard asserts that no `IN_DEVELOPMENT.txt` exists anywhere. It now asserts the rule behind it: a flag may sit only in a method folder whose method has no active `SUPPORTED` entry, and never in E_1's.

These two are test-only changes. Without them every method package would have to edit them again; the reviewer may prefer a different form.

**Unchanged:**
- every CODE-1 and CODE-2 library module, the reader, the coordinator and its protected functions, E_1, the launchers and the wrappers;
- E_6's existing `NOT_YET_SPECIFIED` chain. It stays as the placeholder; real variants get their own chains (E2R-1; `test_append_only_chain`).

**Switches and allowlist:** the four switches stay False, and the allowlist stays empty.

**No per-method entry file (owner decision D6-1, RECOMMENDED):** a contract method is launched by the shared runner (`Run_Experiment.bat Method_Contract_Runner.py run ...`), so it needs no `E_006_<Name>.py` in `src/methods/`. Its code is self-contained in its folder, which is all the template copies.
- This narrows NAMES-1 OPEN-N1 "A" for contract methods only: the entry file there is the shared runner. E_1's legacy entry file is unchanged.
- H-1 v1r4 section 9, step 3, says an entry file is needed; this decision corrects that, and the next register records it.

## 4. Release (E2R-R57, R58; owner decision D6-3)

- **This package installs E_6 non-runnable:** the flag file is present, and all six entries are `FORMULA_OPEN`. The dispatch gate refuses every E_6 request (`NOT_SUPPORTED`), and the roster shows E_6 as `FORMULA_OPEN`.
- **Release 1, a later small reviewed package:**
  - it deletes `IN_DEVELOPMENT.txt`;
  - it appends `entry_0002` `SUPPORTED` for `BETA_BERNOULLI_FULL_MEMORY_V1` in both games;
  - nothing else.
- **Release 2** appends `SUPPORTED` entries for the two decay variants. It is registry only, with no code and no flag change, and can ride with the E_3/E_4 round.
- **Releases are not authorisation for real data.** `ENABLE_CONTRACT_REAL_DEVELOPMENT` stays False. Released E_6 variants run on synthetic workspaces only.

## 5. Real data and scoring: what is still missing (owner decision D6-4, for information and planning)

To "see what happens" on the real development draws, three things are needed, and none exists yet:
1. **Real-data contract runs:** an owner decision to turn on `ENABLE_CONTRACT_REAL_DEVELOPMENT`, with its own review. It would cover the development prefix only, with the holdout sealed.
2. **A walk-forward driver:** one standalone run per development target, for one method variant. This is orchestration only. It is not the coordinator, so the P2 kill path is not involved.
3. **The R3 scorer and a first report:** matches per draw, divisions and MR7 against the fair-draw expectation, as R3 section 17 specifies.

**Recommendation:** a separate package, "WF-1", after E_6 release 1 and before or alongside E_3/E_4. E_6 and E_1 would be its first two methods, and E_1 is a known baseline. This note only plans it.

## 6. Tests and proof

**6.1 E_1 match (the lead-method oracle).** For both games and several targets, on varied synthetic masters:
- E_6 `FULL_MEMORY`'s `ranked_groups` must equal E_1's equal-count groups in E_1's order;
- its probabilities must equal (r + count) / (1 + n) exactly, as fractions converted once to float.

**6.2 The worked example** (section 2.6), exactly, for both lambdas.

**6.3 Exact normalisation:** for every variant, game and target tested, the exact sum is s_B, and the float vector is within the declared 1e-12.

**6.4 No peeking (T-05 for E_6):** the rows at and after the target are rewritten in three ways. The record's canonical content must be byte-identical across all three.

**6.5 Through the contract, under a simulated release.**
- Test harness only: a copy of the installed registry with `SUPPORTED` appended, and a method folder without the flag.
- Each variant in each game runs through `run_contract_method` to SUCCESS, and `read_run` consumes the run.
- `verify` recomputes independently by a different exact algorithm (a Horner-style recursion, k <- lambda k + x) and refuses any difference.

**6.6 As installed:**
- every E_6 request is refused before any data is read (`NOT_SUPPORTED`);
- with a `SUPPORTED` entry but the flag present, the request is refused with `IN_DEVELOPMENT_FLAG_PRESENT`;
- the roster shows E_6 as `FORMULA_OPEN`;
- the variant table in the code equals the six installed declarations;
- the E_6 files pass the existing symbol-aware import firewall: no reader or data-folder reference.

**6.7 Mutation checks** (planted defects in disposable copies), each caught by a test. The candidate has 14:
- a prior not centred on r;
- a prior worth more than one draw;
- the weight anchored at the oldest draw instead of the newest;
- off-by-one ages;
- a float `pow` in place of the exact power;
- a variant table entry changed;
- `verify` comparing nothing;
- every variant computed as full memory. This one passed every test at first, because `verify` shares the variant lookup. It exposed a missing test, now added: each variant's output against the formula computed in the test itself;
- the probability vector out of label order;
- the method opening a file (a route to data beyond its view);
- the drawn-order view accepted;
- the runner not listing E_6;
- the flag deleted without a release;
- an entry installed as `SUPPORTED`.

**6.8 The whole suite:** 190 existing tests plus E_6's 20, so 210, and the install run-through on both Pythons, LF and CRLF.

## 7. The new-method template (draft 1)

**Where:** `doc/METHOD_TEMPLATE/`. It sits outside `src/`, so it can never be imported or run. Its files are plain text copies, `*.py.txt`, so no tool treats them as code.

**Contents:**
- `README.md`: what the template is for, and the step-by-step checklist from idea to release. Each step names the file, the field and the reason.
- `METHOD_SPECIFICATION_TEMPLATE.md`: the fill-in specification. It has one numbered section for each choice R2 and E2R-1 require:
  - what is modelled;
  - the rule;
  - sparse data;
  - normalisation;
  - outputs per barrel and the probability justification;
  - exactness and platform identity;
  - variants and their fixed settings;
  - a worked example;
  - relation to other methods;
  - the tests.

  E_6's own specification (section 2) is the filled-in example.
- `method_folder/__init__.py.txt`, `method_folder/model.py.txt`, `method_folder/contract.py.txt`, `method_folder/IN_DEVELOPMENT.txt`: E_6's files with the E_6 specifics replaced by `FILL IN:` markers. Each says what goes there and why. Everything else says "leave alone", with the reason.
- `declaration_example.json` and `registry_entry_example.json`: E_6's, annotated in the README field by field.
- `test_template.py.txt`: the test layout. It includes a guard test that fails while any `FILL IN` marker remains in the copied method, so a half-done copy cannot pass.

**Status:** DRAFT 1. It is revised after E_3/E_4 (the shared-helper and score-only cases) and proved by the E_7-E_16 batch.

**A trial use, already done (author evidence):** in a scratch tree, Claude built a throwaway "E_7" by copying the template and filling in its markers (with E_6's mathematics under new variant names). The template's generic tests (no peeking, runs through the contract, as-installed refusal, folder guards) passed, and with two methods installed the existing suite still passed.
- The trial found one brittle test of E_6's own: it pinned the runner's exact list of methods. That is fixed, and the README now warns about it.
- The trial method was never part of the package.

## 8. Owner decisions

- **D6-1 (RECOMMENDED): no per-method entry file for contract methods (section 3).**
- **D6-2 (RECOMMENDED): E_6 revision 1 and its settings:** the Beta-Bernoulli rule, the one-draw fair prior, and the three variants with their lambdas (section 2). This is the method-level approval R2 7.1 requires.
- **D6-3 (RECOMMENDED): the release plan (section 4):** install non-runnable; release 1 for `FULL_MEMORY` only; release 2 for the decay variants.
- **D6-4 (for planning): real data and scoring, as package WF-1 (section 5).** No action now.
- **D6-5 (RECOMMENDED): the template:** draft 1 under `doc/METHOD_TEMPLATE/`, reviewed with this package.

## 9. The speculative candidate

Built from `f9de54a` in Claude's workspace, and held for review after this design passes:
- the files of section 3;
- the tests of section 6;
- the template of section 7;
- an install package in the CODE-2 pattern: verifier with PRE, POST and COMMITTED, the suite runner, exact diffs, the mutation tool and evidence.

Its evidence is listed in the EX message that carries it.

## 10. Not in scope, and gates that stay closed

- **Not in scope:** real-data runs, walk-forward, scoring, Oz Lotto science, FINAL, holdout, coordinated runs, retirement tooling (CODE-3) and any change to E_1 or to the contract libraries.
- **Gates that stay closed:** no switch or allowlist change, and nothing touching `source_data/`, `results/` or `transitory_data/`.
- **The orphan-marker rule** applies unchanged.
