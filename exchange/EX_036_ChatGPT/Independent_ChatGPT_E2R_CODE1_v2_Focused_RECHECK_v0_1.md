# Independent ChatGPT E2R-CODE-1 v2 Focused RECHECK v0.1

Date: 2026-10-29
Project: hydra3333/analysing_perceived_randomness_in_reality
Reviewer: ChatGPT independent reviewer
Input: EX_035_Claude.zip and embedded E2R_CODE1_Install_v2.zip
Scope: E2RC1-B01, E2RC1-C01, E2RC1-C02 (EX_034); HIGH-tier code recheck.

## Verdict

PASS for the three EX_034 findings. 0 BLOCKER, 0 CORRECTION, 0 OPTIONAL,
0 RECONSIDER in this focused recheck. Recommend owner consideration of the
CODE-1 v2 implementation, subject to separate owner ratification, the final
install package, the owner's full Windows acceptance, and Git verification.
No code installation or additional execution authority is granted.

## Submitted package and mechanical evidence

- EX_035_Claude.zip: SHA-256
  f8371df3afa1d6dfe401694c0259553e8533da9e6492c54229f613e14f930d86.
- E2R_CODE1_Install_v2.zip: SHA-256
  f21f7d753167059ed50b324ea57474b36c5168e92016477f91f22287e1d1380f.
- BASE_2f4e84e_src_tests.zip: SHA-256
  3c5001b5840d9a609fb770829c50be2ccd8a71d79303a5b5adab2a685c4c740b.
- v2: exactly 156 repo_overlay files. Its manifest names the other 155;
  all 155 Git/LF SHA-256 values independently matched the ZIP payload.
  The manifest member itself is the 156th file and its stored SHA-256 is
  12cde936b9d3ebc9e96c255dc33d31eed1c3b763f4815b8c8f288461d304d030.
- v1/v2 comparison: 143 paths common; 140 byte-identical, exactly 3
  code/test paths changed, 13 v2-only evidence/review paths and 10
  retired v1-path evidence files.
- The three changed files are:
  src/methods/_common/contract_registry.py
  src/methods/_common/contract_receipts.py
  tests/test_e2r_contract.py
- Independently applied code_v1_to_v2.diff to those three v1 source files
  in disposable scratch space. All three results are byte-for-byte equal
  to v2 after CRLF-to-LF normalisation. No other existing CODE-1 overlay
  code/data file changed. The 126 registry JSON records and the register
  v0.11 candidate remain unmodified.
- No independent live Git fetch was used for base 2f4e84e; the supplied
  archive hash and the prior v1 package establish this reproduction scope.

## E2RC1-B01 - PASS; RECHECK completed

Location: contract_registry.py, InstalledRegistry and _frozen/_thaw.
The prior nested MappingProxyType wrappers have been replaced with canonical
bytes in read-only outer mappings, tuples of immutable (digest, bytes) entries,
__slots__, and read-only ordinary instance assignment. Each public record
accessor deserialises a fresh caller-owned mapping and verifies its canonical
bytes and SHA-256 identity. Accessors cover declarations, chains and the active
entry. Mutation of a returned copy cannot alter the loaded registry or later
copies. Loader and chain validation occur before canonical-byte storage.

Independent tests:
- RegistryImmutability: 3/3 PASS; includes nested declaration and
  entry mutations, alias separation, no writable ordinary instance state,
  and raw stored-content identity checks.
- Remaining CODE-1 contract module (excluding T12): 52/52 PASS.

Future CODE-2 review watchpoint (not a new finding): the execution gate must
re-fetch/validate the installed registry entry rather than trusting a caller-
mutated copy. Python's normal encapsulation is not a security boundary against
arbitrary malicious introspection; this library's claim is stable values
for ordinary callers and checked record identities.

## E2RC1-C01 - PASS; RECHECK completed

Location: contract_receipts.py, _UTC_TIMESTAMP and _utc.
A full-match ASCII grammar requires YYYY-MM-DDTHH:MM:SS followed optionally
by 1-6 fractional digits and a single Z. datetime.strptime validates the
calendar and time, refusing impossible dates and leap seconds. Both freeze
and diagnostic receipt validators use this common check. Timestamps remain
informational only; they are not evidence of prospective publication time.

Independent tests:
- ReceiptTimestamps: 2/2 PASS, checking both receipt kinds, each with
  five valid and 25 invalid values, including the three EX_034 examples.
- No unexpected acceptance observed in the supplied negative cases.

## E2RC1-C02 - PASS; FIX AND PROCEED completed

Location: INSTALL_INSTRUCTIONS.md and RUN_E2R_SUITE.py.
The instructions now say 138 rather than v1's incorrect 132/133. This is
correct for v2: the unchanged 84-test baseline plus 53 CODE-1 contract
tests (48 previous plus five new) and one T-05/prefix test. The expected
module counts in the runner sum to 138. The exact v1-to-v2 instructions
diff also records package-path/count updates. Accept the expanded 138 total
as the intended version-specific documentary correction; no further
independent documentary recheck is required.

## Independent offline reproduction (Linux, Python 3.13.5)

All testing took place in a disposable copy assembled from the supplied
baseline src/tests archive and v2 overlay. No real source_data was provided.

Module                                                   Passed / Expected
--------------------------------------------------------------------------
tests.test_multigame_static_and_timing                         6 / 6
tests.test_multigame_launch_and_manifest                      11 / 11
tests.test_multigame_exit_receipt                             18 / 18
tests.test_multigame_science_allowlist                          6 / 6
tests.test_multigame_console_and_synthetic_scorer              7 / 7
tests.test_t05_hardening                                        2 / 2
tests.test_e1_align                                            5 / 5
tests.test_e1_standalone                                      13 / 13
tests.test_multigame_windows_lifecycle_review                   6 / 6
tests.test_e2r_contract (excluding six-worker T12)            52 / 52
tests.test_e2r_prefix                                          1 / 1
--------------------------------------------------------------------------
TOTAL                                                        127 / 127

All these independently completed tests passed, with zero skips. The
three B01 and two C01 new tests are among the 52 contract-module tests,
not five additional tests on top of the 127.

Not independently completed:
- 10 tests in tests.test_multigame_reader_contracts require real master
  inputs, intentionally not delivered. They were not attempted.
- The T12 six-worker synthetic determinism test was not completed here.
  An aggregate attempt including it stalled and hit the environment's
  execution timeout; it was excluded from the subsequent controlled run.
  This is NOT a test failure finding and is NOT an independent PASS.
- Thus independent coverage is 127 of the 138 prescribed tests, not the
  complete 128 available without real masters.
- Claude separately reports 138/138 on Linux 3.13.17 and 3.15.0b4,
  16/16 mutation checks, synthetic R-4 oracle agreement, and disposable-
  clone installation trials. These remain author-side evidence; I did not
  independently reproduce the full 960-output oracle or all install phases.

## Reviewer decisions (explicit)

E2RC1-RD-05: CLOSE E2RC1-B01, PASS. The deep-immutability correction meets
its focused RECHECK requirement.
E2RC1-RD-06: CLOSE E2RC1-C01, PASS. Both receipt kinds now strictly reject
malformed UTC representations; this meets the focused RECHECK requirement.
E2RC1-RD-07: CLOSE E2RC1-C02, PASS, FIX AND PROCEED. Accept v2's 138-test
count in the documentation as the natural successor to the v1 correction.
E2RC1-RD-08: PASS the bounded v2 CODE-1 focused RECHECK and recommend owner
consideration, preserving the unperformed Windows/real-master acceptance
and final installation gates. No departure from ratified rules authorised.

Claude should report RD-05..08 to the owner under the current reviewer-
decision reporting practice. The eight always-review subjects retain
mandatory independent RECHECK; no waiver is granted by this review.

## Final boundaries

Register v0.11 is still a candidate, not owner-ratified or installed.
The v1 installation ZIP is superseded and MUST NOT be installed.
The owner remains sole ratifier/execution authoriser and committer outside
the previously agreed exchange/ exception. CODE-2 and CODE-3 are separately
gated. This review did not authorise installation, release, real-data
scientific execution, holdout opening, beacon retrieval, dependency upgrade,
process termination, safety-switch change or any Git write.

End of independent CODE-1 v2 focused recheck.
