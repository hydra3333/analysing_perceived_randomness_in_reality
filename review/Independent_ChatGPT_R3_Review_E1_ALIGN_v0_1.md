# Independent ChatGPT R-3 Design Review - E1-ALIGN v0.1

Date: 2026-10-28
Project: hydra3333/analysing_perceived_randomness_in_reality
Reviewer: ChatGPT, independent reviewer
Source: EX_003_Claude.zip, including Predictive_Randomness_E1_ALIGN_Specification_v0_1.md
Review tier: HIGH (reader / N-1 static firewall and orphan-marker path)
Verdict: REVISIONS REQUIRED before owner ratification
Findings: 1 BLOCKER, 1 CORRECTION, 1 OPTIONAL, 0 RECONSIDER

## 1. Scope and verification

The uploaded ZIP is SHA-256
0dda622e96c933c639e29273286c4b710d2861c705e1848296fb78d5d7589b24.
The archive is flat, all eleven members are ASCII with CRLF, and all ten
attachment hashes in its EX_003 contents table match in both shipped CRLF and
canonical LF forms. The specification's LF SHA-256 is
9791188e7f6a9e66b9f135875bc15ebd6e4a6793c777e275f9b91d28f35cafe5.

Reviewed the complete specification, proposed 14-file diff, counted edit
script, new static guard tests, author-side checker and reported test evidence.
The supplied diff is design evidence, NOT an installed source change. Its five
moves and shared-function extraction are internally consistent with the design.
No project test, lottery-data access, orphan-marker operation, scientific run,
source migration or Git write was performed by this reviewer. I did not
independently reproduce Claude's Linux trial or inspect the complete base tree
at commit 38fc60e; 84 OK / 22 PASS are author-reported and not Windows proof.
This review evaluates the supplied specification and candidate source diff;
actual implementation against the eventual installed NAMES-1 base remains a
separate mandatory HIGH-tier RECHECK.

## 2. Design strengths accepted in principle

- The shared reader's legacy E_1 digest uses generic canonical encoding
  without importing the E_1 method; legacy view identity stays unchanged.
- Only canonical_bytes and the length32 tuple framing move to _common.
  E_1's method-specific TIE_SHA256_V1 implementations remain with E_1.
- The E_1 entry file stays flat; five E_1-specific modules move into E_001/
  while keeping their e1_ names, compatible with owner option A.
- e1_standalone_contract moves byte-identically and the containing folder
  remains at the same depth below the project root: parents[3] still names
  the project root. T07 plus the unchanged module and mutation is a sensible
  nondestructive design-stage check; real interlock behavior remains governed
  by pre-existing acceptance tests and mandatory later code review.
- The discovery of SIX canonical JSON encoder copies, rather than three,
  is valuable. A comparison against a fixed canonical oracle, including
  invalid inputs and Unicode, is preferable to merging them now. Extraction
  of the coordinator's pure encoder by AST avoids importing the coordinator.
- R04 correctly refuses to introduce any E2R release admission gate early.
- T10-T12 correctly preserve E_1 goldens, reader isolation, protected ASTs,
  safety switches and comprehensive Windows acceptance (84 applicable tests,
  with actual expected skips accounted for rather than guessed).

## 3. Findings

### E1A-B01 - BLOCKER - The proposed firewall can pass prohibited reader imports

Location: specification section 5, E1A-R07 and E1A-T09; trial diff for
`tests/test_multigame_static_and_timing.py`, in
`test_method_loader_import_firewall_except_accepted_legacy_e1`.

The new AST loop appends `node.module` for ast.ImportFrom but does not inspect
`node.names`. Therefore the expression

    from _common import game_draws_reader

in an E_002 method file has module `_common`; the guard sees no
`game_draws_reader` token and incorrectly permits it. Python can resolve the
reader submodule through this form.

The exact E_1 bridge exception is also currently keyed only by module and
count. Replacing its permitted import

    from _common.game_draws_reader import DrawView

with

    from _common.game_draws_reader import load_pinned_draw_view

would still count one allowed import from `_common.game_draws_reader`, even
though it exposes a reader loader instead of the accepted DrawView type.
Appending an extra imported symbol on that same statement also evades its
single-statement count. Both outcomes contradict the proposed exact
file/kind/reference/count exception and its N-1 isolation intent. The eight
reported mutations do not exercise these cases.

Required replacement: E1A-R07 and its test must identify BOTH the module and
the imported symbol(s) for ImportFrom statements, including `from _common
import game_draws_reader`. The only accepted method-folder reader import must
be exactly one `DrawView` import from `_common.game_draws_reader` in the one
named E_1 bridge file; no additional names, aliases that broaden capability,
or other reader import forms. Keep the entry-file grandfathering unchanged
unless the owner explicitly changes E1A-D3. Add fail-closed mutations for all
three counterexamples above, and show the unchanged control passes. Clarify
that the static test is a regression guard, not a comprehensive defence
against obfuscated dynamic imports: the separate exact-diff review remains
mandatory.

Disposition: RECHECK. This concerns the protected reader / N-1 boundary and
cannot receive FIX AND PROCEED. Do not ratify R07/T09 in their current form.

### E1A-C01 - CORRECTION - The trial checker does not prove an exact edit allowlist

Location: specification E1A-R01, section 3.3, E1A-T01/T02;
`e1align_checks.py`, regular expression `IMPORT` and `allowed()`.

The author-side checker accepts ANY changed line matching its general import
regular expression, without comparing the exact old and new import/module
names from section 3.3. Its firewall special case similarly accepts a broad
class of lines within the test body. This confirms that changes resemble
imports or a firewall edit, but does NOT alone establish the specification's
claim that every changed line is from the exact authorised list. The supplied
trial diff itself looks consistent with the advertised changes; this is an
assurance-evidence issue, not evidence of an unauthorised edit.

Required replacement: specify that the later package's read-only acceptance
verifier checks the complete old-path/new-path mapping and exact expected
old/new text (with counts and no extras), verifies the five moved files and
the two moved function bodies, and rejects every unlisted changed line in
code/tests. A SHA/diff may be retained as delivery evidence, but do not use
broad regex categories as the sole proof of the exact allowlist. Report the
results against the actually installed NAMES-1 predecessor, not only the
current disposable trial tree.

Disposition: RECHECK, because the proof gates the shared-reader code change.

### E1A-O01 - OPTIONAL - Qualify callable metadata equivalence

Location: E1A-R02, R03, T02/T05 and the new canonical_encoding.py.

Alias binding preserves E_1's `canonical_bytes` and `_length32_tuple` callable
behavior and identity with the NEW shared callable. It does not preserve the
functions' historical `__module__` metadata; the public tuple function also
changes `__name__` from `_length32_tuple` to `length32_tuple`. These are
intentional structural differences, not changes to canonical output bytes.
State explicitly that the structural exception covers callable metadata and
import paths, while freezing serialization, prediction and tie results. If
reflection, pickling or fully qualified callable names are used as persistent
identities, they need separate checks; do not silently assert all properties
of the old callable object are byte-identical.

Disposition: FIX AND PROCEED only for a precise non-normative explanation;
any actual code/test change or normative expansion is RECHECK. Omission of
this optional note need not by itself block design acceptance after B01/C01.

## 4. Owner decisions, requested scope and gates

E1A-D1: Recommend the owner accept E_1 revision 1 ONLY as the narrowly scoped,
explicit E1-ALIGN structural exception, conditional on complete unchanged
scientific identities and acceptance evidence. No automatic inheritance from
NAMES-1 or precedent for substantive edits.

E1A-D2: Recommend the owner confirm NAMES-1 -> E1-ALIGN -> E_2-readiness code,
with amendment to the record of E2R-R59's earlier sequencing. Do not install
E1-ALIGN before owner-approved, independently checked NAMES-1.

E1A-D3: Recommend the owner retain the existing complete entry-file exemption
for THIS structural migration, while imposing the corrected exact counted
allowance on E_001 folder modules. This is not blanket permission for future
entry-file changes.

This design review authorises no implementation, archive operation, test run,
release, scientific computation, access to draw outcomes or holdout data, or
Git action. Later code is HIGH tier and mandatory RECHECK under the eight
always-review subjects regardless of line count.

## 5. REVIEWER-DECIDED (extended owner oversight)

E1A-RD-01: Retain HIGH-tier classification and a separate mandatory
independent implementation RECHECK.
E1A-RD-02: Identify E1A-B01 as BLOCKER; require symbol-aware negative reader
firewall checks and RECHECK.
E1A-RD-03: Identify E1A-C01 as CORRECTION; require exact, independent,
change-list verification in the later package and RECHECK.
E1A-RD-04: Classify E1A-O01 as OPTIONAL documentary clarification, with the
limited FIX AND PROCEED disposition stated above.
E1A-RD-05: Support E1A-D1/D2/D3 for owner consideration ONLY under the
specified proof and timing constraints; no owner decision inferred.

Please report every item RD-01 through RD-05 to the owner under the extended
oversight arrangement. No departure from ratified controls is authorised.
The proposed firewall gap would constitute a protection failure if installed
unfixed; it is identified before ratification.

## 6. Requested next handoff

Prepare narrowly corrected E1-ALIGN v0.2 and send the updated specification,
exact v0.1-to-v0.2 diff, response matrix and evidence of the revised negative
firewall mutants. Keep the source movement, six-encoder oracle and E_1 science
unchanged. No broad rewrite or additional scientific work is requested.

End of review.
