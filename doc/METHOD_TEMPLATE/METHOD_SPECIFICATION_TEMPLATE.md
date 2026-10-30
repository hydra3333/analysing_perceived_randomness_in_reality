# Predictive Randomness - E_<n> specification (<method name>), v0.1

**FILL IN** the header:
- **Document:** the method-level specification of E_<n>'s variants (R2 v0.5 section 7.1), and the design of the package that adds them.
- **Version:** v0.1 DRAFT for the reviewer's design-stage review (R-3), <date>. Author: <chat>. Ratifier: the project owner.
- **Status:** it authorises nothing, and it changes no ratified rule.
- **Base:** the `main` commit the package is built on.

E_6's specification (`doc/Predictive_Randomness_E6_Specification_and_Method_Template_Design_v0_1.md`, section 2) is the filled-in example of every section below.

## 1. In plain English

**FILL IN:**
- What question does the method ask of the history, what does it compute for each number, and how does that become TOP and WORST?
- What do its outputs mean, and what do they not mean?
- Why is it worth testing? Under the owner's philosophy no idea is excluded, but a claim needs a testable form.

## 2. What is modelled

**FILL IN** the random variable, per barrel: what is observed at each eligible draw (inclusion, gap, position, order...) and which view it needs.
- `UNORDERED_SET`, `OPERATOR_DRAWN_ORDER` or `PAIRED_DIAGNOSTIC`.
- Dates or not. A method that uses dates halts when a source date and a derived date disagree.

## 3. The rule

**FILL IN** the exact formula, with every symbol defined:
- the model family;
- the treatment of sparse data (labels never yet seen, short histories);
- the normalisation. Say why it holds exactly, or how far it can drift and how that is handled; the contract's tolerance is 1e-12 unless the reviewer agrees otherwise.

## 4. Outputs, per barrel

**FILL IN** each barrel's channel:
- the ranking kind (`RANKING_WITH_SCORES`, `RANKING_ORDER_ONLY` or `NONE`), and the score type;
- the TOP and WORST rules: `TOP_MARGINAL`/`INVERSE`, or `MAP_SET`/`INVERSE_FROM_MARGINALS`, and so on (E2R-R15A);
- the probability kind, its tolerance, its smoothing note and its calibration note;
- the minimum history, any diagnostic record, whether the fit is stochastic (a stochastic fit needs a reviewed seed policy, which does not exist yet), and the fit-model version tag.

**FILL IN the probability justification**, if it publishes probabilities (R2 7.1: "only if justified"): under which model they are exact or approximate, and what they ignore.

## 5. Exactness and platform identity

**FILL IN:** why the record is byte-identical on Windows and Linux (exact arithmetic, or, for an iterative floating-point fit, the objective proof and the canonical output and tie rules; README, "published values must be byte-identical").
- **Answer explicitly:** does any step repeat until a condition holds (narrowing bounds, a search, an iteration)? Say why it ends for every input, including exact ties and exact zero, and what its cap does.

## 6. Variants (fixed now)

**FILL IN** a table: `variant_id` (`[A-Z0-9_]{3,96}`, ending `_V1`), its settings, and what it means.
- Each variant is declared for each game it can run in.
- A method using both barrels together is `UNSUPPORTED_FOR_GAME` for Oz Lotto. Never invent a Powerball barrel.

## 7. Worked example

**FILL IN:** a tiny case small enough to check by hand, with exact expected values for every variant. Compute the values with a reference script, not by hand, and ship the script with this specification. The tests check them exactly.

## 8. Relation to other methods

**FILL IN** any overlap with other methods, stated plainly, for example "with setting X it ranks exactly like E_1". Overlap is reported (rank correlation), never a reason to exclude.
- **Answer explicitly:** does any variant rank exactly like an installed method (README, "the same-count ranking trap" and "the sign trap")? If so, what distinguishes it: its probabilities, its window, its settings? Is any claimed equivalence with another formulation proved, not assumed (README, "changing a covariate")? The tests check every claimed relation by comparing `ranked_groups`.

## 9. What the package adds and changes

**FILL IN:**
- the new files;
- the replaced files, each listed;
- what is unchanged;
- that the four switches stay False and the allowlist empty.

## 10. Release

**FILL IN:** installed non-runnable; which variants each release package makes `SUPPORTED`; real data stays a separate gate.

## 11. Tests and planted defects

**FILL IN:**
- the tests (README step 8);
- the planted defects, one or more per property claimed, per variant setting and per verification rule (README step 10);
- whether anything found should change this template (owner, 30 October 2026).

## 12. Owner decisions

**FILL IN** each decision as question / why / recommendation / options. Label each one RECOMMENDED, DECIDED (with its authority) or OPEN.

## 13. Not in scope, and gates that stay closed

**FILL IN:**
- real-data runs, scoring, holdout, FINAL and coordinated runs, unless separately approved;
- no switch or allowlist change;
- the orphan-marker rule applies unchanged.
