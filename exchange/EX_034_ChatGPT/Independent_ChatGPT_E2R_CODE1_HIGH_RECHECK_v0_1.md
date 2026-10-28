# Independent ChatGPT HIGH-tier RECHECK - E2R-CODE-1 v1

Date: 2026-10-28
Project: hydra3333/analysing_perceived_randomness_in_reality
Role: ChatGPT independent reviewer
Input: EX_033_Claude.zip and E2R_CODE1_Install_v1.zip
Status: REVISIONS REQUIRED for CODE-1; register v0.11 content acceptable conditionally.

## 1. Verified inputs and scope

EX_033_Claude.zip SHA-256:
  d84a241f9ecd7b16119c71bde1c7ea0d8192351082c6c51a69e0ea984f866d0c
E2R_CODE1_Install_v1.zip SHA-256:
  acb9f0ea475697d3b073bae84f7d7fff06d791e04ee2e3c869a1abf5cf5876fb
Base named by author: 2f4e84e1d8454e847fdfd7d8e832adb0d0187460.

ZIP integrity: both PASS. The overlay has exactly 153 files and the
INSTALL_MANIFEST_SHA256.txt lists exactly those 153 paths; 153/153 LF-canonical
SHA-256 comparisons PASS. No pre-existing repository path is overlaid.
Six contract modules, 126 canonical JSON files, 3 test modules/fixtures and 18
documents/evidence files are present. The JSON inventory comprises 2 E_1
scientific declarations and 124 registry entries (2 SUPPORTED E_1 and 122
FORMULA_OPEN E_2..E_62), across the two games.

The candidate register v0.11 SHA-256 is
  16a29efcea651c8a6cbf5e1e93cfe9347e94f91a3bc1cf1264222bcc935519ae
as LF-canonical Git content. Reverse-applying the supplied register diff
reconstructs installed v0.10 exactly, SHA-256
  8ee8307e3c98eabbf24743391c7ebb821e6700f8efa8a093996f97d3d43475a4.
This supports the register's history and new E1-ALIGN and CODE-1 section.

No actual GitHub baseline fetch was successful in this session. Thus the
published base commit and guarded source-blob hashes are AUTHOR assertions,
not independently verified against remote Git. The installer enforces those
identities when run on the owner's checkout.

## 2. Findings: E2R-CODE-1

### E2RC1-B01 - BLOCKER; RECHECK: the registry's declared immutability is shallow

Location: src/methods/_common/contract_registry.py, especially lines 63-68,
74-84, and the class documentation at lines 40-41.

The loader exposes `self.declarations` and `self.chains` using
`MappingProxyType`, but the values inside these proxies are ordinary mutable
Python dictionaries, nested lists and dictionaries. This does not deliver
the stated read-only scientific declarations or append-only in-memory
registry records. For example, a caller can change:

  registry.declarations[digest]['channels']['MAIN']['top_rule_id']

without an exception, or change:

  registry.chains[key][1]['text_provenance']['author']

The recorded digest/registry key remains the previously computed one. A
consumer that reuses these objects may therefore observe a changed declared
scientific rule or provenance under an unchanged identity. Later recomputation
may reject it, but that is not a sufficient replacement for the promised
immutable interface, and CODE-2 will depend on these objects.

Independent evidence: in an isolated reviewer process, the submitted
InstalledRegistry loaded all 2 declarations and 124 chains with synthetic,
mocked profile metadata. Mutating both nested fields above succeeded. The
reviewer did not alter on-disk data or installed repository files.

Required: make the exported declaration and active-entry interfaces truly
immutable at all depths OR keep mutable internal structures inaccessible and
return defensive, independently validated copies. In either case specify
who may retain and mutate returned copies, ensure stored digests cannot be
silently divorced from governing values, and add negative tests that attempt
nested mutation of channels, observation views and text provenance. Preserve
existing canonical record identities and stage-1 registry semantics. Exact
code change to return for focused independent RECHECK.

### E2RC1-C01 - CORRECTION; RECHECK: non-UTC values pass frozen_at_utc validation

Location: src/methods/_common/contract_receipts.py lines 37-45, `_utc`;
exercised via `_common_receipt` and both receipt validators.

The function only checks the last character `Z`, then parses the preceding
text with datetime.fromisoformat. It accepts each of the following invalid
UTC timestamp representations:

  2026-10-28T12:30:00+10:30Z
  2026-10-28Z
  2026-10-28T00:00:00-05:00Z

I extracted the exact `_utc` function AST and executed these three purely
synthetic cases: all were accepted. The first and third encode a nonzero
numeric UTC offset and also claim to be UTC. The second is date-only, not a
timestamp. This conflicts with the explicit `frozen_at_utc` contract field.

Required: validate a genuine UTC date-time with explicit clock time and a
single `Z`, no embedded timezone/offset, rejecting malformed and impossible
dates. A strict grammar plus a real datetime parse is suitable. Preserve
valid precision explicitly (integer seconds or fractions, if supported).
Add positive and negative tests for both forecast and diagnostic receipts.
The timestamp remains informational, NOT independent proof that publication
predated an outcome (E2R-R40C). This is freeze-contract code and is RECHECK.

### E2RC1-C02 - CORRECTION; FIX AND PROCEED: wrong expected suite count

Location: E2R_CODE1_Install_v1/INSTALL_INSTRUCTIONS.md, section 2.

The sentence says `SUITE PASS (132 tests; ... )` whereas RUN_E2R_SUITE.py
expects 84 pre-existing + 48 contract + 1 prefix = 133, and EX_033 also
states 133. Replace only `132 tests` with `133 tests`. Preserve every other
byte of the installation instructions. This is a precisely specified,
non-normative explanatory correction; FIX AND PROCEED at reviewer discretion.
Its diff and hash must be retained in the next handback.

## 3. Findings: Register v0.11

REGISTER CONTENT: PASS for this design/records stage, 0 new content findings.
Its proposed CODE-1 installation history and ratification-candidate wording
must remain prospective until the CODE-1 corrections have passed independent
review and the owner ratifies and actually installs the revised package.
Normal exact finalisation and subsequent Git verification still apply.
Do not treat this content assessment as owner ratification of register v0.11.

## 4. Scope and independent reproduction limitations

The following passed independently:
- both ZIP integrity checks, all overlay/manifest hashes and exact file count;
- reverse-diff reconstruction of the ratified register v0.10 content;
- canonical JSON inventory counts and an isolated registry loader smoke test;
- exact-AST isolated `_utc` mutation probes, including the invalid values;
- nested-mutation probes against actual CODE-1 registry objects with mocked
  game profiles; no real draw, holdout, or source_data file was read.

The following remain AUTHOR-REPORTED and were not independently reproduced:
- Linux 133-test suite on Python 3.13.17 and 3.15.0b4;
- 12/12 mutation catches;
- 192-case independent oracle preparation and 960 exports (the author's log
  says the 48 invariance contexts and planted-leak check passed);
- disposable-clone LF/CRLF installation trials and six negative stops;
- live GitHub baseline/guarded-blobs verification.

The complete E2R-T03/T05 suite requires the already-installed reader,
profiles and other existing repository modules. Those dependencies are not
in these two ZIPs and could not be fetched here. I have not claimed their
acceptance or run the T12 six-worker ProcessPoolExecutor test. R-2
reproduction therefore remains PARTIAL. The owner's Windows 133-test run,
including the specifically announced T12 process spawning, remains a later
separate gate and is NOT authorised by this review.

Design boundaries preserved: CODE-1 supplies uncalled contract modules and
canonical data; no reader, coordinator, launcher or safety switch is changed.
The method-facing task excludes orchestration-only master hashes. Stage-1
reserved modes, seed policies and unsupported method placeholders remain
restricted. The code-level changes above must not be treated as authorising
CODE-2 dispatch or scientific execution.

## 5. REVIEWER-DECIDED and dispositions

E2RC1-RD-01: Preserve the HIGH-tier independent CODE-1 review and require
focused RECHECK of the nested-immutability blocker and UTC correction.
E2RC1-RD-02: Permit the sole 132->133 documentation correction as
FIX AND PROCEED, with exact diff/hash and no expansion.
E2RC1-RD-03: Accept the register v0.11 candidate's CONTENT conditionally;
no inferred ratification, CODE-1 installation or W-23 execution gate.
E2RC1-RD-04: Record independent R-2 reproduction as PARTIAL; keep the owner's
complete Windows suite, T12 process notice and normal installation gates.

No departure from the owner's ratified restrictions is authorised. In
particular the eight always-review subjects are RECHECK-only for code.

## 6. Decision and next handback

CODE-1: REVISIONS REQUIRED: 1 BLOCKER, 2 CORRECTIONS, 0 OPTIONAL,
0 RECONSIDER. Do not recommend owner installation of this candidate.
Register v0.11: CONTENT PASS, but final ratification and install pending.

Claude should prepare a narrowly corrected CODE-1 candidate with exact
code diffs, updated manifest and ZIP hash, negative tests for the two code
findings, and documentary proof of the 132->133 change. Return the code
corrections for focused RECHECK; there is no request to redesign the E2R-1
specification, revise existing E_1 algorithms, or run real scientific data.

End of independent review.
