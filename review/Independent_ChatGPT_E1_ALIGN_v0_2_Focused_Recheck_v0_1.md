# Independent ChatGPT focused RECHECK - E1-ALIGN v0.2

Date: 2026-10-28
Project: hydra3333/analysing_perceived_randomness_in_reality
Reviewer: ChatGPT independent reviewer
Source: EX_006_Claude.zip, file Predictive_Randomness_E1_ALIGN_Specification_v0_2.md
Risk: HIGH (shared reader, N-1 import boundary and orphan-marker location)
Verdict: TARGETED REVISION REQUIRED
Findings: 0 BLOCKER / 1 CORRECTION / 0 OPTIONAL / 0 RECONSIDER

## 1. Integrity and evidence

The EX_006 ZIP SHA-256 is 84e6f8ebe4d4d992df7ec84dbad8cdc65b56b32cf58af8a9cc9022e02b981678.
The supplied E1-ALIGN specification is CRLF as shipped and has verified LF SHA-256
c08c1e9cba7d5f2a9a4c5560bcd4b670f12ede8ceac96ebcfb253e0b644a3ee6.
Its v0.1-to-v0.2 diff reverse-applies with zero fuzz to reproduce original
v0.1 SHA-256 9791188e7f6a9e66b9f135875bc15ebd6e4a6793c777e275f9b91d28f35cafe5,
matching the original EX_003 attachment. All evidence-member identities listed
in EX_006 were checked; shipped/canonical exceptions for intentionally CRLF
CMD and instruction files are correctly distinguished.

The reported 84 Linux tests and 22 checker PASS results are Claude's author-side
evidence. I examined the proposed test source, exact allowlist, diff and records;
I did not independently execute project code or reproduce the Linux tests.
The future actual NAMES-1 installation remains a separate prerequisite.

## 2. Original EX_004 findings

E1A-B01: CLOSED at design stage. The revised method-file reader firewall
checks ImportFrom module AND imported symbol, forbids aliases, extra symbols,
and other forms outside the exact one-file DrawView allowance; text counts and
mutations m9-m15 give appropriate regression evidence. It explicitly does not
claim complete detection of obfuscated dynamic imports.

E1A-C01: CLOSED at design stage. The frozen e1align_allowlist.json defines
exact text blocks, file moves and added-file identities. The proposed verifier
checks the installed NAMES-1 predecessor and rejects extra edits and files.
This is a meaningful replacement for v0.1's overly broad import-like regex.

E1A-O01: CLOSED. E1A-R02A explicitly qualifies intentional callable __module__
and __name__ changes while preserving scientific output identities.

## 3. New finding: E1A2-C01 - CORRECTION - E1A-T04 ignores imported names

Location: proposed tests/test_e1_align.py, helper _imports(path), and
E1AlignGuards.test_shared_code_imports_no_method_code; specification
E1A-R05 and E1A-T04 (sections 2, 6), E1A-T09.

The helper yields only node.module for ast.ImportFrom, not the names/aliases.
For example, a shared module containing:

    from methods import E_001

has ImportFrom.module == 'methods' and imports E_001 by name. The current
E1A-T04 checks 'methods', sees no E_ prefix and passes. Likewise
'from _common import e1_training_view' evades its E_1-only name check.
This is a static, independently reproduced counterexample, not a claim that
the actual submitted sources contain either import. It is different from the
method-file reader firewall E1A-B01, which v0.2 fixes correctly.

Required narrow correction: when an ImportFrom is visited in the shared-code
guard, inspect the module and EACH imported name (including star imports and
aliases as relevant). Reject imports of E_<nnn> packages or named E_1-only
modules through either path. Add a controlled negative case to E1A-T04/T09
injecting 'from methods import E_001' into a shared module, with unchanged
control PASS. Keep the already corrected method-file reader firewall and its
exact file-specific allowances unchanged. Do not broaden the exception or
alter E_1 science.

Disposition: RECHECK. The proof concerns shared->method dependencies and the
reader/N-1 architectural boundary; no FIX AND PROCEED is available for code
in the eight always-review subjects.

## 4. Owner decisions and boundaries

Continue to recommend E1A-D1/D2/D3 for express owner decision: E_1 revision 1
only under a separately ratified E1-ALIGN structural exception with the
complete equality proof; NAMES-1 then E1-ALIGN then E_2 code; existing E_1
entry-file exemption and exact E_1 bridge/training-view allowances only.
Do not activate E2R runtime admissions in E1-ALIGN. The protected coordinator,
three switches, allowlist, tie logic, goldens, orphan marker and real-data
firewall remain unchanged. Implementation requires its OWN HIGH-tier code
RECHECK and the owner's Windows 84-test acceptance.

## 5. Explicit REVIEWER-DECIDED (continuing the same E1-ALIGN review)

E1A-RD-06: Close prior E1A-B01, E1A-C01 and E1A-O01 at design stage on the
v0.2 evidence, without approving future implementation.
E1A-RD-07: Classify E1A2-C01 as CORRECTION with RECHECK; require symbol-aware
shared-code import tests and a fail-closed negative.
E1A-RD-08: Retain HIGH tier, the three owner decisions, later Windows acceptance
and mandatory independent implementation review. No ratified safety deviation.

Please have Claude inspect each REVIEWER-DECIDED item under the indefinite
owner oversight/reporting-by-exception process. This is a continuation of the
same E1-ALIGN design review, not a new independent work item.

No code, data, holdout, scientific run, process or Git operation was performed.
