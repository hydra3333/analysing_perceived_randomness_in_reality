# Predictive Randomness - E1-ALIGN specification, v0.2

**Document:** the design for E1-ALIGN, which brings E_1 into the same source layout as every later method (owner decision OPEN-N1 = A, and the owner's acceptance in principle of E1-ALIGN, both 28 October 2026).
**Version:** v0.2 DRAFT for focused RECHECK, 28 October 2026 (Adelaide, UTC+10:30). v0.2 answers the R-3 review of v0.1, `Independent_ChatGPT_R3_Review_E1_ALIGN_v0_1.md` (`5a11390971289e23237ec6839d7530ada4bec1b9134c248fbddeee7eaae45197`, in EX_004; 1 BLOCKER, 1 CORRECTION, 1 OPTIONAL). Section 11 lists the changes.
**Author:** Claude (primary designer and coder). **Independent reviewer:** the ChatGPT reviewer chat. **Ratifier:** the project owner.
**Status:** DRAFT. A design only. It authorises no move, no source change and no run. The E1-ALIGN code package follows only after this design is reviewed and ratified, NAMES-1 is installed, and the owner authorises the package.
**Base:** commit `38fc60e03ea0766f72476cbab7c0e1eb5bd59d07` **with the NAMES-1 v0.2 renames applied** (`07bda3e4a8a99bfc611a76cec672f8642532186567737e1a23de5e5701489e5a`). All names and line numbers below are post-NAMES-1. The code package will be rebased on the actual NAMES-1 commit.
**Risk tier:** HIGH. E1-ALIGN changes an import in the shared reader, rewrites the static import-firewall test, and moves the module that holds E_1's orphan-marker check. The code package always gets an independent RECHECK.
**Holdout statement:** no draw outcome appears here. Design evidence used only the accepted offline synthetic suite, in disposable copies.
**Inputs:** the reviewer's early comments, `Independent_ChatGPT_E1_ALIGN_Early_Design_Comments_28Oct2026.md` (`0cf83504ecd35440cc35723d74dcafab5c58b4dbd33c7feb3daaca3b475021af`), on Claude's proposal (`244aac86c72ff696e1d658023de8ab14035f2bb732585467bd140830e461cb59`). Section 10 shows where each comment is answered.

**Tags.** **DECIDED** cites an owner decision or ratified text; **RECOMMENDED** is a design choice proposed for ratification; **OPEN** is a decision for the owner, with a recommendation. Requirement IDs are `E1A-Rnn`; tests are `E1A-Tnn`.

---

## 1. Purpose in plain English

After NAMES-1, every method's entry file sits directly in `src/methods/`, and each later method keeps its own modules in its folder `src/methods/E_<nnn>/` (option A). E_1 would be the one exception, with its own modules in the shared `_common` folder, and with the shared reader borrowing a function from E_1's module. The owner's principle is that **shared code must not depend on a method, because a method may validly change.**

E1-ALIGN fixes both, and changes nothing about what E_1 computes:
- the two genuinely generic encodings move from E_1's module into a shared module;
- E_1's five own modules move into `src/methods/E_001/`.

## 2. Principles and decisions

- **E1A-R01 (RECOMMENDED).** E1-ALIGN moves files, moves two function definitions unchanged, updates imports and `mock.patch` targets, and rewrites the static import-firewall test to scan method folders (section 5). It changes nothing else. Every changed line is on the exact list in section 3.3. No schema, record identity, golden, scientific constant or output byte changes.
- **E1A-R02 (OPEN, E1A-D1; E2R-R14A).** E_1 keeps **revision 1**, under a structural-migration exception that the owner ratifies for E1-ALIGN itself. E2R-R14A names NAMES-1 as its one exception, so that exception does **not** carry over. The conditions of this one:
  - E1-ALIGN does only what section 3 lists;
  - the moved definitions are byte-identical (E1A-T02);
  - every E_1-facing symbol still resolves, and to the same object (E1A-T05);
  - the full proof of section 6 passes, including Windows.

  If any behaviourally relevant implementation changes, the package cannot claim the exception: E_1 gets revision 2, or the owner reconsiders expressly. This is not a precedent for substantive change.
- **E1A-R02A (RECOMMENDED; reviewer's E1A-O01; explanatory).** The exception covers import paths and callable metadata. It freezes what E_1 computes: serialisation bytes, view digests, prediction and tie results.
  - After the move, the two moved functions report `canonical_encoding` as their `__module__`, and the tuple helper's `__name__` becomes `length32_tuple`. These are intended structural differences.
  - The project uses neither as an identity: no record, digest or registry stores a callable's module or name, and nothing is pickled.
  - The claim is equal behaviour and output bytes, not that every attribute of the old function object is unchanged.
- **E1A-R03 (DECIDED by the code; recorded here).** The two moved functions are behaviourally relevant shared helpers under E2R-R14A, since they are encoding. Moving them unchanged is the structural act the exception covers. Their bytes, and the bytes they produce, do not change.
- **E1A-R04 (DECIDED; E2R-R57, R58).** E1-ALIGN activates no gate. It adds no `IN_DEVELOPMENT.txt`, no registry entry and no dispatch check.
  - The SUPPORTED-and-no-flag admission rule arrives with the separately authorised E_2-readiness code.
  - Leaving E_1's folder without a flag is a layout fact, not a permission to run.
  - Every existing gate stays exactly as it is: the three switches False, the allowlist empty, E_1's own real-mode gate, and the orphan-marker checks.
- **E1A-R05 (DECIDED; reviewer's early comment).** No shared module may import method code. A test enforces that for `_common`, `coordinator_private` and the coordinator (E1A-T04).
- **E1A-R06 (RECOMMENDED).** The protected coordinator, `coordinator_private`, the launch wrappers and the owner tools are not edited. The coordinator's own encoder copy is read by the new test from its source (AST), never imported or run.

## 3. What changes

### 3.1 Moves

| Old path (post-NAMES-1) | New path |
|---|---|
| `src/methods/_common/e1_historical_appearance_frequency.py` | `src/methods/E_001/e1_historical_appearance_frequency.py` |
| `src/methods/_common/e1_training_view.py` | `src/methods/E_001/e1_training_view.py` |
| `src/methods/_common/e1_standalone_contract.py` | `src/methods/E_001/e1_standalone_contract.py` (byte-identical) |
| `src/methods/_common/e1_common_reader_bridge.py` | `src/methods/E_001/e1_common_reader_bridge.py` |
| `src/methods/_common/multigame_e1.py` | `src/methods/E_001/multigame_e1.py` |

The `e1_` prefixes are kept. They mark E_1-only responsibility and avoid a second rename straight after NAMES-1; the reviewer agreed. The entry file `src/methods/E_001_Historical_Appearance_Frequency.py` stays where it is, as the Option F wrapper requires.

### 3.2 New files

- `src/methods/_common/canonical_encoding.py`: `canonical_bytes` and `length32_tuple`, moved from E_1's core module. Their bodies are byte-for-byte unchanged. The only text change is that the tuple helper's `def` line drops its leading underscore, because it is now a public shared name.
- `src/methods/E_001/__init__.py`: a one-line docstring, for package traversal (E2R-R55).
- `tests/test_e1_align.py`: five guard tests (E1A-T04 .. T08).

### 3.3 Edited lines (exact)

| File | Change |
|---|---|
| `E_001/e1_historical_appearance_frequency.py` | the two definitions removed; one import added, `from _common.canonical_encoding import canonical_bytes, length32_tuple as _length32_tuple`, so every existing E_1 caller and symbol is unchanged |
| `_common/game_draws_reader.py` (line 108) | `from _common.e1_historical_appearance_frequency import canonical_bytes` becomes `from _common.canonical_encoding import canonical_bytes` |
| `E_001/e1_common_reader_bridge.py` | `from .game_draws_reader import DrawView` becomes `from _common.game_draws_reader import DrawView`: the bridge is no longer in the reader's package |
| `E_001/e1_training_view.py`, `E_001/multigame_e1.py`, the entry file | `_common.e1_*` imports become `E_001.e1_*` (2, 1 and 2 lines) |
| `tests/test_e1_standalone.py`, `test_multigame_reader_contracts.py`, `test_multigame_console_and_synthetic_scorer.py` | the same import and `mock.patch` target updates (5, 6 and 1 lines) |
| `tests/test_multigame_static_and_timing.py` | the firewall test body, section 5 |

E_1's core module keeps `import json`, now unused, so that no further line changes (RECOMMENDED; trivially removable if the reviewer prefers).

## 4. What does not change, and why

- **The tie functions stay with E_1** (`tie_digest`, `rank_counts`, `multigame_e1._digest`). The TIE_SHA256_V1 rule is project-wide, but these implementations hard-code E_1's identity and Powerball's label ranges. A method-generic tie helper is new E_2-readiness code. If E_1 later adopts it, that is a proved, separately reviewed change.
- **The reader's legacy E_1 view schema stays in the reader.** It is a frozen identity, and the reader now imports no method code to build it.
- **The other five encoder copies stay as they are.** The live code has six copies of the canonical JSON encoding:
  - the shared `canonical_bytes`;
  - `multigame_standalone_contract.json_bytes`;
  - `experiment_console_and_file_output.canonical_json`;
  - `e1_standalone_contract.canonical_json`;
  - the exit receipt's `_canonical`;
  - the coordinator's `canonical_bytes`.

  Claude's proposal counted three; checking the code found six. E1A-T08 is a regression alarm across all six, not licence to change any of them. Merging them is a later owner option.
- **E_1's orphan-marker check is unchanged.** `e1_standalone_contract` locates the project marker as `Path(__file__).resolve().parents[3] / 'transitory_data' / 'poc_runs' / 'UNRESOLVED_ORPHAN.json'`. `_common/` and `E_001/` are at the same depth, so the path is unchanged. E1A-T07 proves it by path arithmetic only: no marker is ever created, read or removed.
- **Out of scope:**
  - the owner's data tools and the legacy test scripts (as NAMES-1 OPEN-N2);
  - `review/`, `doc/` and `transitory_data/`.

## 5. The import firewall, widened and made symbol-aware (E1A-R07, RECOMMENDED; corrected in v0.2)

Today's static test checks only `src/methods/*.py`. It skips E_001's entry file as a whole, and forbids any other file from importing the shared reader or naming `source_data`. It has two weaknesses:
- **Method folders escape it.** Under option A, files in a method folder would not be checked. E1-ALIGN creates the first method folder, so the widening belongs here.
- **It reads only the module part of `from X import Y`** (reviewer's E1A-B01). So `from _common import game_draws_reader` passes it. That gap is **already present in the committed test at `38fc60e`**: a probe `src/methods/E_999_Probe.py` containing `from _common import game_draws_reader_v1` passes it today (evidence `v0_1_firewall_gap_demonstration.txt`). No current method uses that form; E1-ALIGN closes it. NAMES-1 leaves the test's logic unchanged.

The rewritten test:
- **Scope:** `src/methods/*.py` **and** `src/methods/E_[0-9][0-9][0-9]/**/*.py`.
- **Grandfathering:** E_001's entry file stays exempt as a whole, exactly as today (E1A-D3), because it is accepted frozen code.
- **Every reader import is identified by form, module, imported name and alias.** For `from M import N [as A]`, each imported name is checked: the import is a reader import if M **or** N contains `game_draws_reader`. For `import M [as A]`, M is checked.
- **Every textual mention is counted.** In each scanned file, the occurrences of `game_draws_reader` and of `source_data` are counted. A string-based dynamic import is therefore caught too.
- **Exact allowances.** Inside `E_001/`, only these are allowed, nothing is allowed by folder, and every allowance must be used:

  | File | What | Exact allowance |
  |---|---|---|
  | `E_001/e1_common_reader_bridge.py` | import | `from _common.game_draws_reader import DrawView`, no alias, once; no other name from the reader |
  | `E_001/e1_common_reader_bridge.py` | text | `game_draws_reader`, 1 occurrence (that import line) |
  | `E_001/e1_training_view.py` | text | `source_data`, 1 occurrence (its accepted trusted-folder check) |

- **Anything else fails.** That includes a new file inside `E_001/`, another import form, an extra or different imported name, an alias, or a star import.
- **What it is not.** It is a static regression guard, not a complete defence against deliberately obfuscated dynamic imports, such as a module name built up from pieces. The exact-diff review of every package remains mandatory.

## 6. Proof plan

| Test | What it proves |
|---|---|
| E1A-T01 | **Exact change set, against a frozen allowlist** (corrected in v0.2, reviewer's E1A-C01). `e1align_allowlist.json` is part of the reviewed design. It lists the five moves, the three added files with their SHA-256, the one file moved unchanged, and, for each of the ten edited files, its edits as exact (old block, new block) pairs. Each old block carries enough unchanged context to occur exactly once. At install, the read-only verifier works against the **installed NAMES-1 predecessor**: it rebuilds every new file from its predecessor using only those blocks, and requires byte equality. It fails on any unlisted file, edit, addition or deletion. Broad categories such as "looks like an import" are not proof. |
| E1A-T02 | **Moved-code equality.** Both moved definitions appear byte-for-byte in `canonical_encoding.py`; only the tuple helper's `def` name changes. `e1_standalone_contract` is byte-identical. |
| E1A-T03 | **AST equality**, as N1-T03, for every edited module, with the import changes applied. |
| E1A-T04 | **Shared code imports no method code.** No import in `_common`, `coordinator_private` or the coordinator names an `E_<nnn>` package or an E_1-only module. |
| E1A-T05 | **E_1's symbols are the shared functions.** `E_001.e1_historical_appearance_frequency.canonical_bytes` **is** `canonical_encoding.canonical_bytes`, and its `_length32_tuple` **is** `length32_tuple`. The reader imports the shared module. |
| E1A-T06 | **Location and origin, in fresh interpreters** (as N1-T05). Each moved module imports from `E_001/`, with `__file__` there; the old `_common` names are refused; no old file remains. |
| E1A-T07 | **The orphan-marker path is unchanged**, by path arithmetic only. |
| E1A-T08 | **Six-encoder regression alarm.** On a fixed corpus (nested, key order, Unicode including U+2028 and astral characters, control characters, integer and float boundaries, tuples, integer keys), all six copies give the bytes of the stated canonical rule. All six reject the same invalid inputs: `NaN`, infinities, sets, bytes and mixed key types. The coordinator copy is extracted by AST. |
| E1A-T09 | **Mutations**, in disposable copies, with the unchanged tree as control. Each of these is rejected:<br>- from v0.1: a new `E_001/` file importing the reader; `import _common.game_draws_reader` in `E_002/`; `source_data` in `E_002/`; a second `source_data` in an allowed E_1 file; an unused allowance; the reader importing E_1 code again; a changed shared encoder; a moved orphan-marker path;<br>- added in v0.2 for E1A-B01: `from _common import game_draws_reader`, in `E_002/` and in a new `E_001/` file; the bridge importing `load_pinned_draw_view` instead of `DrawView`, even under the alias `DrawView`; the bridge importing an extra reader symbol; the bridge aliasing `DrawView`; a star import from the reader; a string-based `importlib.import_module` of the reader in `E_002/`.<br>The exact checker of E1A-T01 also rejects three edits made to its own trial: an extra comment on an allowlisted line, a different import that still looks like an import, and an unlisted new file. |
| E1A-T10 | **E_1's science is unchanged.** The legacy goldens and identity vectors, the prefix-only and view regressions, T-05, the standalone contract tests and the multi-game E_1 tests all pass unchanged. |
| E1A-T11 | The eleven protected coordinator ASTs are unchanged (TH-1, no skip); the three switches are False; the allowlist is empty. |
| E1A-T12 | **Windows, all 84 current tests.** The 60 tests of NAMES-1, plus the 5 of `test_e1_align`, make 65 in the standard suite; then the 19 others. The owner runs them on Python 3.14 with the per-module reporter, and with the NAMES-1 N1-T09 rules for counts and symlink skips. No destructive, lifecycle or process test is added. |
| E1A-T13 | **Install-time recovery check**, as N1-T10: a disposable clone, while the commit exists. |

**The new standard suite:** the NAMES-1 seven modules plus `tests.test_e1_align`, with the same `PYTHONPATH`.

## 7. Design evidence (author-side trial; not the package)

The NAMES-1 map was applied to a disposable export of `38fc60e`, then `apply_e1align.py` (counted, exact edits) and `test_e1_align.py` were added. These are Claude's own Linux trials (Python 3.13.17), not Windows acceptance:
- **All 84 tests OK**, no skips, per module: 10, 6, 11, 18, 6, 7, 2, 5, 13 and 6. All of E_1's goldens are unchanged.
- **`e1align_checks.py` (v0.2): 22 checks, all PASS.** They cover:
  - the exact-allowlist check: 10 edited files, 22 blocks, 5 moves, 3 added files;
  - the moved bodies;
  - three negatives against the checker itself;
  - the control;
  - fifteen mutations.
- **`v0_1_firewall_gap_demonstration.txt`** shows the gap is real: the v0.1 proposed test accepts the reviewer's three counterexamples, and the committed test accepts the same import form.
- **The exact trial diff** (`e1align_trial_names1_to_e1align.diff`) covers 14 files: 208 lines added and 42 removed. Git detects the five moves as renames.

## 8. Records that go out of date

- **E2R-R59's order.** The ratified order is: specification, then NAMES-1, then the E_2-readiness code. The owner has inserted E1-ALIGN after NAMES-1 (E1A-D2).
- **E2R-R14A**, which names NAMES-1 as its only structural exception (E1A-D1).
- H-1's module map; register v0.7's out-of-date line on Architecture's layout; Architecture's "one standalone `.py` per method", which now has E_1's entry file plus its folder.

The register edition installed with E1-ALIGN records these; the next H-1 and Architecture editions fold them in.

## 9. Decisions for the owner

**E1A-D1 - Keep E_1 at revision 1 under a structural exception scoped to E1-ALIGN?**
- **Recommendation: yes,** on the conditions of E1A-R02. The reviewer agrees, provided the exception is ratified for E1-ALIGN explicitly.

**E1A-D2 - Confirm the order: NAMES-1, then E1-ALIGN, then the E_2-readiness code.**
- **Recommendation: yes,** recorded as an amendment of E2R-R59's order.

**E1A-D3 - E_1's firewall exemption.**
- **Recommendation:** keep the entry file exempt as a whole, as today, and allow exactly the two references of section 5 inside `E_001/`. Removing the entry-file exemption would mean changing accepted E_1 code, which would be E_1 revision 2.

## 10. Where the reviewer's early comments are answered

| Comment | Answer |
|---|---|
| Q1: move only the generic encoders; keep E_1's tie code | Sections 3.2 and 4; E1A-T05 keeps the old E_1-facing symbols, by alias |
| Q2: guard test, not a merge; the contract as oracle; invalid inputs too | E1A-T08, across all six copies found; the coordinator is not edited (E1A-R06) |
| Q3: keep `e1_` prefixes | Section 3.1 |
| Q4: own owner-ratified structural exception; exact transformed-source proof | E1A-R02, E1A-T01 .. T03, E1A-D1 |
| Caution 1: no early E2R gate activation | E1A-R04 |
| Caution 2: narrow, explicit E_1 firewall allowance; same-folder probe | Section 5; E1A-T09 |
| Caution 3: the reader must not import method code; HIGH tier; Windows evidence; no hashes or Git dependence | E1A-R05, E1A-T04, E1A-T12; nothing records a hash or commit |

## 11. Changes from v0.1 (response to EX_004)

| Finding | Response |
|---|---|
| E1A-B01 (BLOCKER): `from _common import game_draws_reader` and bridge symbol substitution not caught | Section 5 rewritten: symbol-aware import identification; exact allowance by file, form, module, name, alias and count; textual counts of both words; a stated regression-guard limit. Mutations m9..m15 added to E1A-T09. The same gap was found in the committed test and is closed by E1-ALIGN |
| E1A-C01 (CORRECTION): checker accepted any import-like line | E1A-T01 now uses a frozen exact allowlist (`e1align_allowlist.json`), applied against the installed NAMES-1 predecessor; three checker negatives |
| E1A-O01 (OPTIONAL): callable metadata | New E1A-R02A (explanatory) |

Nothing else changed: the moves, the shared module, the tie functions staying with E_1, the six-encoder guard, the orphan-marker path and E_1's science are as in v0.1.

*End of E1-ALIGN specification draft v0.2.*
