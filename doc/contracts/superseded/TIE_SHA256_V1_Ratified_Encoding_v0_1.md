# Shared tie-key byte encoding: TIE_SHA256_V1 (record of owner decision)

**23 October 2026.** **Authority:** the owner ratified D2, independently verified by Claude against the E_1 v0.3 written specification and golden vectors. This note consolidates that existing decision for all methods; it is not a revision to ratified R3 v0.2. R3 section 2.4 controls the conceptual tuple/readout policy. An inconsistency must be raised, not resolved by silently altering a version.

## Exact tuple, byte representation and sorting

For label `j` in one barrel, in this exact order:

1. domain `PREDICTIVE_RANDOMNESS/TIE_SHA256_V1`
2. permitted training-view SHA-256 (64 lowercase hexadecimal characters)
3. target draw identifier (canonical nonnegative base-10 ASCII digits, no sign or leading zeroes)
4. method ID (for the lead: `E_1`)
5. stable variant ID (for the lead: `FULL_HISTORY_RAW_COUNTS_V1`)
6. barrel identifier (`MAIN` or `POWERBALL`, uppercase exactly)
7. ranking tie-readout version `TIE_SHA256_V1`
8. label (canonical nonnegative base-10 ASCII digits, no sign or leading zeroes)

Encode each field as `uint32 little-endian UTF-8 byte count` followed by exactly those UTF-8 bytes, concatenated without separators. Compute SHA-256 over the concatenation. In tied native scores, place the **ascending digest** first (rare collision: ascending numeric label). Native score remains primary descending key. The inverse WORST order is the exact reversal of the one frozen complete ranking; evaluator-only mid-ranks apply to equal *native scores before* digest tie breaking. This encoding is explicit and must not vary with machine endian mode, Python object representation or wall-clock time.

## Independently confirmed synthetic vector (not a real forecast)

From E_1 v0.3 invented synthetic fixture (`p3_e1_synthetic_v0_3.json`), training target 1152:

- permitted *synthetic* view digest `df21871f8067e5405b4fdb1eec50c65dddbaa35958872bad3230d3c10a791fd4`
- MAIN label 3 tie digest `7ce5ab1bae014adf61f1f02dd152d4b500cb405b65cb3886cdcee8dd9e2c9932`
- synthetic canonical forecast digest `7b43d659d611791deb14d106a72984f153d9f79cc63b3d25000365de4c811d1e`
- TOP `[1,8,2,6,3,7,9]`; WORST `[23,26,18,30,24,25,12]`; Powerball TOP/WORST `1/9`.

These vectors apply **only** to E_1's v0.3 synthetic view and original v0.3 canonical format. A new production U-view domain/version intentionally has different content digests and therefore different tie readout, even over the same invented draw values. Do not substitute these synthetic digests as real canonical-view identities.

**Status:** D2 itself OWNER-RATIFIED, this note is a new packaging/traceability candidate awaiting acceptance and repository installation.
