# New-method template (draft 2)

**What this is:** the files and the step-by-step checklist for adding a new method to the project, taken from E_6 (the first method built on the E_2-readiness contract) with its specifics stripped out.
**Status:** DRAFT 2, 30 October 2026, by Claude. Draft 1 was written with E_6; draft 2 adds what E_3 and E_4 taught (a shared helper, scores only, a minimum history) and what the design of wave 1 (E_7, E_8, E_9, E_10) found. It is reviewed with wave 1's design.
**Kept up to date** (owner, 30 October 2026): whenever a method's design, review, code or install shows something this template should say or do differently, in Claude's assessment or the reviewer's, Claude proposes the update in the next package, and it is reviewed like any other document. Each method's handback says whether it found anything for the template.
**Authority:** none. The rules are in E2R-1 v0.3r3, R2, R3 and the current ratification register; where this file differs from them, they win. Using the template authorises no run.

Everything here is outside `src/`, so it can never be imported or run. The code files end in `.py.txt` for the same reason. When you copy one, drop the `.txt`.

## How the pieces fit

A method needs only its own pieces. The shared contract does the rest:
- **The release rule:** a method runs only if an active `SUPPORTED` registry entry is pinned by the request, and there is no `IN_DEVELOPMENT.txt`. A refusal reads no data.
- **The prefix-only view:** the method sees only draws before the target.
- **Ranking, ties and readout:** the contract ranks the scores, applies `TIE_SHA256_V1`, and reads TOP and WORST from the one frozen ranking.
- **Record validation:** every record is checked by recomputation.
- **Publication:** create-only publication, receipts and terminal records.

**The method's own pieces:**

| Piece | Where | From this template |
|---|---|---|
| Its specification | `doc/`, reviewed and owner-ratified | `METHOD_SPECIFICATION_TEMPLATE.md` |
| Its mathematics | `src/methods/E_<nnn>/model.py` (name it for what it does), or a shared helper in `src/methods/_common/` used by several methods | `method_folder/model.py.txt` |
| Its connection to the runner | `src/methods/E_<nnn>/contract.py` | `method_folder/contract.py.txt` |
| Its package marker and flag | `src/methods/E_<nnn>/__init__.py`, `IN_DEVELOPMENT.txt` | `method_folder/` |
| One line in the runner | `src/methods/Method_Contract_Runner.py` | step 6 below |
| Its declarations and registry entries | `src/methods/_common/contract_data/` | `make_contract_data.py.txt` |
| Its tests | `tests/test_e<nnn>_<name>.py` | `test_template.py.txt` |

`<nnn>` is the method number zero-padded to three digits: E_6 is `E_006`, and E_17 is `E_017`. The folder name is only a locator; the method's identity is always `E_n`.

## The checklist

Do the steps in order. Each says what, where and why.

**0. Identity.** Choose the method.
- **A catalogue method E_2..E_62:** it already has a `FORMULA_OPEN` placeholder (variant `NOT_YET_SPECIFIED`). Leave the placeholder alone: real variants get their own registry chains, and the placeholder is never promoted or edited.
- **A new idea:** it needs an identity of E_63 or above, which is an owner decision and a catalogue amendment first.

**1. Specification.** Fill in `METHOD_SPECIFICATION_TEMPLATE.md` as a new document in `doc/`.
- **Fix every variant and every setting now.** After release, any change to the method's code, even adding one setting, is a new revision with archiving (E2R-R14A).
- **Review:** the reviewer gives a design-stage review (R-3), and the owner ratifies before code depends on it.

**2. Copy the folder.** Copy `method_folder/` to `src/methods/E_<nnn>/`.
- Drop the `.txt` endings.
- Rename `model.py` to describe the mathematics (E_6: `beta_bernoulli.py`), and fix the import in `contract.py`.

**3. Fill in the mathematics** (`model.py`), at every `FILL IN:` marker.
- **Or a shared helper:** when several methods need the same calculation (E_3 and E_4: polynomial fits; wave 1: occurrence counts), put it in one module in `src/methods/_common/`, with its own test module, and keep only each method's own rule in its folder. Every method that uses the helper names it in its specification. A change to the helper is a new revision of every method that uses it (E2R-R14A), so fix its behaviour as carefully as a method's.
- **The variant table:** each `variant_id` with its fixed settings.
- **The calculation:** a pure function from the eligible draws to one number per label.
- **Imports:** it imports nothing from the project, reads no file and starts nothing.
- **Exactness:** prefer exact arithmetic (`fractions.Fraction`, integers). If floats are unavoidable, say in the specification why the result is the same on Windows and Linux (no `pow`, `exp`, `log` or summation-order differences), or how the method copes with a last-bit difference.
- **A second, differently written algorithm** for the same quantity, used by `verify()`.

**4. Fill in the connection** (`contract.py`).
- Set `METHOD_ID`, the allowed view and the barrels.
- Return a `MethodOutput`:
  - one `BarrelOutput` per barrel;
  - a `ScoredRanking` if the method gives every label a score, or an `OrderOnlyRanking` if it gives only an order;
  - a `ProbabilityVector` only if the declaration says it has one.
- **Scores only** (E_3, E_4, E_9, E_10): if the values are not chances (a curve can leave [0, 1]; a difference of rates is not a chance), declare `probability_kind` `NONE`, return no `ProbabilityVector`, and say why in the specification and the registry texts. Converting scores into chances by an invented transformation is not "marking"; publishing the scores themselves is.
- **Too little history:** if the eligible draws are fewer than the declared `minimum_history_draws`, return an empty `MethodOutput` (no barrels). The contract then records `INSUFFICIENT_HISTORY`: published, no ticket. `verify()` must accept that record when it recomputes the same shortage, and refuse it otherwise.
- **`verify()`** must recompute independently and refuse any difference. It is the last check before publication.

**5. Keep `IN_DEVELOPMENT.txt`.** It makes the method non-runnable until its release package removes it.

**6. The runner line.** In `src/methods/Method_Contract_Runner.py`, add one import (`from E_<nnn> import contract as e_<nnn>`) and one entry in `ADAPTERS`, and change nothing else in that file. Being listed there is not permission to run: the dispatch gate decides.

**7. Declarations and registry entries.** Copy `make_contract_data.py.txt` to the package's tools (not into the repository), and fill it in.
- **Never hand-write the JSON.** The script validates every record and writes canonical bytes, which the registry insists on. `declaration_example.json` and `registry_entry_example.json` are E_6's records, pretty-printed for reading; installed files are canonical one-line JSON.
- **What it writes:**
  - one `METHOD_DECLARATION_V1` per game and variant: `declarations/<GAME>/E_<n>/<VARIANT>/r1.json`;
  - one `REGISTRY_ENTRY_V1` per game and variant: `registry/<GAME>/E_<n>/<VARIANT>/entry_0001.json`, status `FORMULA_OPEN`, naming its declaration.
- **The plain-English `one_liner` and `short_explanation`** (owner decision D-3) say what the method looks at, how it ranks, what its probabilities mean (or that it has none), and that it is not expected to beat chance if the draws are fair.

**8. Tests.** Copy `test_template.py.txt` to `tests/test_e<nnn>_<name>.py` and fill it in. Keep every test class. They are the minimum:
- the worked example;
- normalisation;
- each variant's own setting;
- the relation to an existing method, if one is claimed;
- no peeking (T-05);
- a run through the contract under a simulated release;
- the installed state refused;
- the folder guard;
- the `FILL IN` guard.

**9. Words to keep out of the method folder.** The import firewall and the folder guard refuse them:
- the reader module's name (`game_draws_reader`) and the data folder's name;
- `open(`, `read_bytes`, `write_bytes`, `subprocess`, `import os`;
- the contract's publication, receipts and runner modules.

They are refused even in comments, because they are checked as text.

**10. Planted-defect (mutation) checks.** For every property the tests claim, plant a defect in a disposable copy and show that a test fails (E_6: 14 defects; E_3/E_4: 27). Plan at least one defect per variant setting and one per verification rule. A defect that no test catches is a missing test: E_6 found one this way (every variant computed as the first), and E_3/E_4 another (a certificate accepting one alternation too few).

**Several methods in one package** (E_3/E_4; wave 1): one shared helper with its own tests, one generator for all the declarations and entries, one test module for the methods, one `ADAPTERS` line per method, and one mutation tool covering all of them. Each method still gets its own folder, flag, variants and registry chains, and is released on its own.

**11. The install package** (code-package discipline: H-1 section 1.6). It contains:
- the overlay;
- a verifier with PRE, POST and COMMITTED, listing each replaced file with its base bytes;
- the suite runner, with each module's expected count;
- the exact diffs, the mutation tool and its output;
- install run-throughs in LF and CRLF clones of the current `main`, on both Pythons.

The package installs the method non-runnable.

**12. Release** (a separate, small, reviewed package; the owner's two deliberate actions, E2R-R58).
- **The first release:** delete `IN_DEVELOPMENT.txt`, and append `entry_0002.json` with `SUPPORTED` for each variant being released.
- **Later variants of the same revision:** registry entries only.
- **Real data is a separate gate:** `ENABLE_CONTRACT_REAL_DEVELOPMENT` stays False until the owner decides otherwise.

## Things that bite (learned on E_6, E_3/E_4 and wave 1)

- **The tie rule includes the method and variant IDs.** Two methods with identical scores can order exactly tied labels differently, so compare `ranked_groups`, not TOP and WORST, when claiming a match.
- **Existing tests may count installed data.** E_6's package changed the last two such tests to rules: the registry-chain count, and "flags only in unreleased method folders". Search the tests for literal counts before adding data.
- **Synthetic masters from the T-05 fixture repeat the same row.** Counting methods need varied invented rows. `test_template.py.txt` has a generator.
- **Don't pin lists that later methods extend.** E_6's first test asserted the runner's exact method list; the template trial showed that the next method would have had to edit it. Assert only your own method's entry.
- **A test that can only pass is not evidence.** Make sure each variant's own setting is tested against the formula computed in the test itself, not through the module's own lookup.
- **The same-count ranking trap.** Every number is at risk in every draw, so all numbers share the same number of draws. Any score given by the same strictly increasing function of each number's count over the same draws (a fixed-strength posterior mean, a fixed-strength credible bound, a fixed shrunk rate) has exactly the ranked groups of counting over those draws: like E_1 over the full history. Count-only scores need not be monotonic in general, and this excludes no deliberately non-monotonic method. Check a new method's ranking against E_1 and against its own family before claiming it differs; if it does not differ, say so and say what does (its probabilities, for example).
- **Forgetting rates can coincide.** A decayed count at E_6's factor ranks exactly like E_6's decay variant. Choose settings that do not duplicate an installed method, or say that they do.
- **Compute every worked example with a tool.** The E_3/E_4 draft had two hand-worked values wrong. Ship the reference script with the specification.
- **Never ask the Claude Code runner to count or filter output.** Ask for the whole output in its report and count it yourself (TASK_T005).
