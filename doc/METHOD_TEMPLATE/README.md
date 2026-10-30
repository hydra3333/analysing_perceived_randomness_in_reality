# New-method template (draft 1)

**What this is:** the files and the step-by-step checklist for adding a new method to the project, taken from E_6 (the first method built on the E_2-readiness contract) with its specifics stripped out.
**Status:** DRAFT 1, 30 October 2026, written with E_6 by Claude and reviewed with it. It will be revised after E_3 and E_4 (methods that share a helper and output scores only), and proved by the E_7-E_16 batch.
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
| Its mathematics | `src/methods/E_<nnn>/model.py` (name it for what it does) | `method_folder/model.py.txt` |
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

**10. Planted-defect (mutation) checks.** For every property the tests claim, plant a defect in a disposable copy and show that a test fails (E_6: 14 defects). A defect that no test catches is a missing test; E_6 found one this way.

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

## Things that bite (learned on E_6)

- **The tie rule includes the method and variant IDs.** Two methods with identical scores can order exactly tied labels differently, so compare `ranked_groups`, not TOP and WORST, when claiming a match.
- **Existing tests may count installed data.** E_6's package changed the last two such tests to rules: the registry-chain count, and "flags only in unreleased method folders". Search the tests for literal counts before adding data.
- **Synthetic masters from the T-05 fixture repeat the same row.** Counting methods need varied invented rows. `test_template.py.txt` has a generator.
- **Don't pin lists that later methods extend.** E_6's first test asserted the runner's exact method list; the template trial showed that the next method would have had to edit it. Assert only your own method's entry.
- **A test that can only pass is not evidence.** Make sure each variant's own setting is tested against the formula computed in the test itself, not through the module's own lookup.
