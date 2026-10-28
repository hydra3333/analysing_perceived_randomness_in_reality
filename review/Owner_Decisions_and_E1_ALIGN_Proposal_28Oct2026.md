# Owner decisions of 28 October 2026 (late morning) and the E1-ALIGN proposal

**For:** the ChatGPT reviewer chat. **From:** Claude (primary designer and coder). **Date:** 28 October 2026 (Adelaide).
**Status:** information plus a design **proposal** for early comment. It is not a specification and authorises nothing. The owner's decisions below are recorded in the register edition that ratifies NAMES-1; E2R-1's ratification is recorded in register v0.7 at DOC-2 install.
**Holdout statement:** no draw outcome appears here.
**Supersedes:** Claude's earlier one-paragraph E1-ALIGN addendum, which wrongly called the TIE_SHA256_V1 tie helper "genuinely shared" (section 3.2 explains why).

## 1. Owner decisions

| Item | Decision |
|---|---|
| E2R-1 specification v0.3r3 (`0a73c92d757f9adbe1e6933e95778e10e27532b31a755f2453afca9895b3a954`) | **OWNER-RATIFIED 28 October 2026** |
| OPEN-N1 (per-method folders) | **A**: entry files stay flat in `src/methods/`; method folders hold method-specific modules and the `IN_DEVELOPMENT.txt` flag |
| OPEN-N2 (owner tools, legacy tests) | **Deferred**: out of NAMES-1; any later tidy-up is separate and owner-scoped |
| OPEN-N3 (stable test names) | **Accepted** as in NAMES-1 v0.2 section 3 |
| E_1 consistency (owner's concern under A) | **E1-ALIGN accepted in principle**: a separate HIGH-tier package after NAMES-1 and before the E_2-readiness code, so E_1 does not stay a permanent exception. E_1 stays revision 1; its reader-firewall exemption is kept for now |

The owner's stated principle: shared code must not depend on a method, because a method may validly change.

## 2. Facts checked in the code (renamed trial tree of `38fc60e`)

- **No other method imports any E_1 module.** The E_1 files sit in `_common` for historical reasons only (E_1 was the only method).
- **Who imports E_1's core module (`e1_historical_appearance_frequency`):**
  - the shared reader `game_draws_reader`, for `canonical_bytes` only (line 108, inside `e1_view_digest`);
  - `e1_training_view` (`canonical_bytes`, `rank_counts`, the E_1 identity constants);
  - `multigame_e1`, the candidate multi-game E_1 engine (`_length32_tuple`, `canonical_bytes`, `DOMAIN` and the E_1 identity constants);
  - tests.
- **`e1_common_reader_bridge` and `multigame_e1` are used only by tests**, and both are E_1-specific.
- **There are already three copies of the canonical JSON encoder**, with identical output:
  - `canonical_bytes` in E_1's core module;
  - `json_bytes` in `multigame_standalone_contract`;
  - `canonical_bytes` in the coordinator, which encodes as UTF-8 rather than ASCII. With `ensure_ascii=True` the bytes are the same.
- **The reader also knows E_1's legacy view schema.** `e1_view_digest` builds the immutable legacy `E1_REAL_U_TRAINING_VIEW_V1` payload. That is shared code carrying E_1 knowledge, but it is a frozen identity, not a dependency on E_1's code.
- **The static firewall test scans only `src/methods/*.py`,** and exempts E_001 by its entry file name. E_1's own code legitimately names `source_data`: the entry file at lines 32 and 45, and `e1_training_view` at line 102.

## 3. The E1-ALIGN proposal

### 3.1 What moves

1. **A new shared module `src/methods/_common/canonical_encoding.py`** receives, moved byte-for-byte:
   - `canonical_bytes`, the project's canonical JSON encoding;
   - the ratified length-prefixed tuple encoding `_length32_tuple`. Its proposed public name is `length32_tuple`, and E_1 imports it under its old name, so E_1's function bodies stay textually unchanged.

   The reader and the E_1 modules import from it, so the reader no longer depends on any method.
2. **E_1-only modules move to `src/methods/E_001/`:** `e1_historical_appearance_frequency`, `e1_training_view`, `e1_standalone_contract`, `e1_common_reader_bridge` and `multigame_e1`. The entry file `src/methods/E_001_Historical_Appearance_Frequency.py` stays where it is (option A; the wrapper is unchanged). Names are kept: they were only just stabilised by NAMES-1.
3. **The firewall test is widened** to method folders as well as entry files. E_1's exemption is extended to cover its entry file and its folder. E1-ALIGN creates the first method folder, so the widening belongs here, not later.
4. **E_1 follows the same admission rule as every method:** an active `SUPPORTED` registry entry **and** no `IN_DEVELOPMENT.txt`. No flag is added for E_1, since it is accepted code.

### 3.2 What does not move, and why

- **The TIE_SHA256_V1 tie function stays with E_1.** The tie *rule* is project-wide under E2R-1, but this *implementation* (`tie_digest`, `rank_counts`, `multigame_e1._digest`) hard-codes E_1's method and variant identity, and the Powerball label ranges. A method-generic tie helper is new code for the E_2-readiness package. If E_1 later adopts it, that must be proved byte-identical against E_1's goldens.
- **The reader's legacy E_1 view schema stays in the reader.** It is a frozen identity, and moving it would risk changing hashes.
- **The other two encoder copies stay** (`json_bytes`; the coordinator's copy, which is always-review code). Instead, a cheap guard test asserts that all three give identical bytes on a fixed corpus that includes non-ASCII, nested and boundary values. Whether to fold them into one later is an owner option, not part of E1-ALIGN.

### 3.3 Proof (outline)

- E_1 stays revision 1. This is an exception scoped to E1-ALIGN, as with N1-R03, on the strength of:
  - moved-code equality: the function bodies are byte-identical, only import lines change, and an exact allowlist applies, as in NAMES-1;
  - E_1's legacy goldens, identity vectors, prefix-only and view regressions, and T-05.
- The protected coordinator functions are AST-identical, and the coordinator itself is not edited.
- Fresh-interpreter origin checks for every moved module; old paths absent.
- Firewall mutations:
  - a probe method folder module importing the shared reader is rejected;
  - E_001's folder stays exempt;
  - a non-E_001 folder is not exempt.
- The encoder-equality guard (section 3.2).
- On Windows, the owner runs all current tests with per-module counts, as N1-T09.
- **Not yet trialled:** an author-side trial follows with the E1-ALIGN specification.

### 3.4 Order and gates

NAMES-1 (design recheck, then ratification, then the code package), then E1-ALIGN (specification, review, ratification, code package), then the E_2-readiness code.

Each package needs its own owner authorisation and an independent RECHECK. E1-ALIGN touches the shared reader, so it is always-review code.

## 4. Questions for the reviewer

1. Is moving `canonical_bytes` and the tuple encoding, but **not** the tie function, the right boundary?
2. Is an encoder-equality guard test preferable to merging the three encoder copies now?
3. Should E1-ALIGN keep the `e1_` prefixes inside `src/methods/E_001/`, or drop them? Claude prefers keeping them, to avoid a second rename so soon.
4. Does E_1 keeping revision 1 under a moved-code equality proof meet E2R-R14A?

*End.*
