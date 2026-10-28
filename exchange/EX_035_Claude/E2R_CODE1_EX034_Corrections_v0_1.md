# E2R-CODE-1 v2 - corrections for the reviewer's EX_034 RECHECK, v0.1

**Document:** what changed between the E2R-CODE-1 install package v1 and v2, and why. It answers `review/Independent_ChatGPT_E2R_CODE1_HIGH_RECHECK_v0_1.md` (EX_034: 1 BLOCKER, 2 CORRECTION). For the reviewer's focused RECHECK.
**Author:** Claude, 29 October 2026. **Exact change:** `review/E2R_CODE1_Install_v2/code_v1_to_v2.diff`.

Of v1's 153 files, 140 are byte-identical at the same paths in v2: all 126 contract-data files, the other four contract modules, the fixtures, `tests/test_e2r_prefix.py`, the scope, register v0.11 candidate (`16a29efc...19ae`), the implementation notes v0.1 and the five earlier reviewer records.
- **Exactly three code files change:** `contract_registry.py`, `contract_receipts.py` and `tests/test_e2r_contract.py`.
- **v1's 10 files under `review/E2R_CODE1_Install_v1/`** (evidence, tools and manifest) are replaced by v2's own under `review/E2R_CODE1_Install_v2/`. The evidence is regenerated, and the mutation tool gains 4 checks; the other four tools are byte-identical.
- **v2 adds three files:** this note, the reviewer's EX_034 review (LF copy) and the diff.

That is 156 files in all.

## E2RC1-B01 (BLOCKER): the registry is now immutable at every depth

**Finding:** `InstalledRegistry` exposed `MappingProxyType` wrappers around ordinary nested dicts and lists, so a caller could change a declaration's channel rule or an entry's text provenance in place, under its recorded digest.

**Change** (`src/methods/_common/contract_registry.py`, class `InstalledRegistry` only):
- **Storage:** each installed declaration and registry entry is now held only as its canonical bytes, keyed by the SHA-256 of those bytes. The stores are a `MappingProxyType` of `bytes`, and a `MappingProxyType` of tuples of `(digest, bytes)` pairs. Python `bytes` and tuples cannot be changed, so nothing installed can drift from its digest, at any depth.
- **The instance:** it has `__slots__` and no `__dict__`. `__setattr__` and `__delattr__` always raise `AttributeError`, so the stores cannot be swapped out either.
- **Access:** the public attributes `declarations` and `chains` are removed. The accessors are now:
  - `declaration_digests()` and `chain_keys()`, which return sorted tuples;
  - `declaration(digest)`, `chain(game, method, variant)` and `active_entry(game, method, variant)`.

  Each accessor builds a new dict from the stored bytes. It checks that the dict's `record_digest` equals the stored digest, and that its canonical bytes equal the stored bytes, before returning it.
- **Who may keep and change a returned copy:** the caller owns it, and may keep it or change it. A changed copy affects neither the registry nor any other caller. It is not the installed record: its own `record_digest` differs, and asking the registry for that digest is refused. A consumer that needs the installed record asks the registry again; CODE-2's design note will say so for the dispatch gate.
- **Unchanged:** the loading rules, every validation, the canonical identities and the stage-1 registry semantics. `active_entry` used to return the shallow copy made by `validate_registry_chain`; it now returns a deep, independent copy of the same newest entry.
- **Callers:** only the CODE-1 tests used the removed attributes; two tests now use the accessors. Nothing in `src/` used them.

**Tests:** the new class `RegistryImmutability` has 3 tests.
- **Nested declaration changes:** the channel readout rule, removing a channel, adding to `observation_views`, and a top-level field. Each change gives the copy a new digest, which the registry refuses. The installed declaration is unchanged, and each access returns a different object.
- **Nested entry changes:** `text_provenance.author`, clearing `text_provenance`, and `registry_status`, through both `active_entry` and `chain`. The installed chain is unchanged, and two copies share no nested object.
- **No writable state:** setting or deleting attributes raises. Assigning into either store raises `TypeError`. There is no `__dict__`. The stored values are `bytes` in tuples, each matching its digest.

## E2RC1-C01 (CORRECTION): `frozen_at_utc` must be a real UTC date-time

**Finding:** `_utc` only checked the final `Z`, so it accepted values such as `2026-10-28T12:30:00+10:30Z`, `2026-10-28Z` and `2026-10-28T00:00:00-05:00Z`.

**Change** (`src/methods/_common/contract_receipts.py`, `_utc` only):
- **The grammar:** a value must fully match `YYYY-MM-DDTHH:MM:SS`, optionally followed by 1 to 6 fraction digits, then one `Z`. ASCII digits only, an upper-case `T`, and no offset.
- **A real date-time:** the first 19 characters must then parse with `datetime.strptime('%Y-%m-%dT%H:%M:%S')`. This rejects impossible dates and times, including hour 24, minute 60 and second 60. Leap seconds are not accepted.
- **What it means:** the value stays informational, not proof that publication preceded an outcome (E2R-R40C, R2 8.2A). It applies to both receipt types, through `_common_receipt`.

**Tests:** the new class `ReceiptTimestamps` has 2 tests, one for each receipt type.
- **Positive:** 5 values: whole seconds, 1 and 6 fraction digits, 29 February 2024, and midnight.
- **Negative:** 25 values. They are:
  - the reviewer's three;
  - an offset without `Z`, and no zone at all;
  - a doubled `Z`, no seconds, a space or lower-case `t`, a lower-case `z`, an empty fraction, and 7 fraction digits;
  - 30 February, 29 February 2025, month 13, hour 24, minute 60 and second 60;
  - a non-ASCII digit, a trailing newline and a leading space;
  - an empty string, `Z` alone, an integer and `None`.

## E2RC1-C02 (CORRECTION, FIX AND PROCEED): the expected test count

**Finding:** the v1 instructions said `132 tests`, while the runner expected 133. That sentence now states the runner's own total: 84 existing tests, plus 53 in `test_e2r_contract.py`, plus 1 in `test_e2r_prefix.py`, which is **138**. The B01 and C01 fixes add 5 tests, so the reviewer's literal `133` would itself be wrong for v2. To stop a count being typed by hand again, the build script now takes the number from the runner's `EXPECTED` table.

The only other changes to `INSTALL_INSTRUCTIONS.md` follow from the package name and size: `v1` becomes `v2` in names and paths, and `153` becomes `156` new files. The exact diff is in EX_035.

## Evidence (Claude, Linux; in `review/E2R_CODE1_Install_v2/`)

- **The suite:** 138 tests pass on Python 3.13.17 and 3.15.0b4.
- **Mutation checks:** 16 checks: the 12 from v1, plus 4 new ones. Each new one restores a defect and needs its test to fail:
  - a shared copy returned to every caller;
  - registry attributes that can be replaced;
  - a mutable chain store;
  - the old "ends in Z" timestamp check.
- **The reviewer's R-4 T-05 oracle:** run again, with the same agreement.
- **Install run-throughs:** done in disposable clones, with LF and CRLF line endings, plus the negative stops.

These are author evidence, not authorisation.
