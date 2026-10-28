# Independent ChatGPT HIGH-tier code/install review - NAMES-1 candidate

Date: 2026-10-28
Project: hydra3333/analysing_perceived_randomness_in_reality
Reviewer: ChatGPT independent reviewer
Source: EX_006_Claude.zip, NAMES1 tools, source/test diff and trial evidence
Risk: HIGH, always-review reader and coordinator paths
Verdict: TARGETED REVISION REQUIRED before install approval
Findings: 0 BLOCKER / 1 CORRECTION / 0 OPTIONAL / 0 RECONSIDER

## 1. Scope and mechanical checks

EX_006 SHA-256: 84e6f8ebe4d4d992df7ec84dbad8cdc65b56b32cf58af8a9cc9022e02b981678.
The 38 attached evidence/tool file identities in the EX manifest match the
uploaded members, using shipped or canonical LF identity as specified.

Examined names1_code_diff_src_tests.diff, names1_allowlist.tsv,
RENAME_FILES.cmd, STAGE_EXACT_FILES.cmd, VERIFY_NAMES1_INSTALL.py,
CHECK_NAMES1_IMPORTS.py, RUN_NAMES1_SUITE.py, the build script, AST/T02
checkers, installation instructions and reported end-to-end logs.

The source/test diff shows 27 git renames, three unchanged-byte renames,
30 impacted files with 93 removed and 93 added lines, and the 94 mapped
substitutions (one line contains two). In the examined hunks, coordinator
changes are import/issuer-file renames and outside protected routines;
reader import names are revised without altering its filtering algorithms.
The receipt issuer and two contract filename identities intentionally change:
old receipts fail closed, not converted. The static reader-firewall weakness
already documented in EX_004 persists temporarily and is not expanded by
NAMES-1; E1-ALIGN must close it as a distinct later HIGH-tier work item.

The read-only verifier is designed to enforce clean predecessor, DOC-2
installation, 27 exact staged renames, pinned overlaid file bytes, unexpected
path refusal, guarded files, an exact committed-file set and a Git blob check.
Its pre/post/committed trial outputs report PASS in LF and CRLF checkouts,
with negative STOP cases and tested immediate recovery. These are Claude-side
Linux/disposable-copy results, not independently repeated Windows acceptance.

The owner still must run all 79 tests under Windows; the two documented
symlink skips are conditional, not presumed. The actual final installer ZIP,
regenerated review artifact, final register and resulting Git commit are not
in EX_006 and cannot be pre-certified by this review.

## 2. Finding: N1I-C01 - CORRECTION - push precedes committed verification

Location: NAMES1_INSTALL_INSTRUCTIONS.md, section 3, ordered command block;
build_names1_install.py, generated INSTALL_INSTRUCTIONS.md block.

The sequence currently is:

    git commit ...
    git push
    python ... VERIFY_NAMES1_INSTALL.py --repo . --phase committed

The committed-phase verifier is the first mandatory check that compares the
FULL final commit path set and resulting Git blobs against the pinned manifest.
Running it only after git push can publish an unexpected/incorrect commit
before the verifier reports STOP. The earlier post-phase check runs before
staging the new content and does not substitute for this final check.

Required exact change: after git commit, run --phase committed, require
COMMITTED PASS, and ONLY THEN allow git push. Retain Claude's post-push remote
verification and N1-T10 disposal-clone rollback proof. For example:

    git commit -m "NAMES-1: ..."
    python "E:\TEMP\NAMES1_Code_Install_v1\VERIFY_NAMES1_INSTALL.py" --repo . --phase committed
    git push
    git rev-parse HEAD

Update generated instructions in build_names1_install.py and final install
instructions. The prior command ordering must not survive in the final ZIP.
This is a procedural/safety correction, not a request for new runtime code,
release machinery or a different migration plan.

Disposition: RECHECK (narrow, on the revised installation commands and final
mechanical identities). A Git push is an external irreversible publication
step; no FIX AND PROCEED is granted for changing the gate order.

## 3. Installation conditions after resolving N1I-C01

- DOC-2 is first installed and independently Git-verified; the installer
  checks its FINAL register hash and the correct ancestor. Its current simulated
  DOC-2 trial alone is insufficient.
- The eventual install ZIP contains the complete 40-file overlay, this review
  only once completed and owner-accepted, and an up-to-date self-consistent
  register v0.8, manifest, verifier and exact staging/rename list. Inspect the
  actual final ZIP's SHA and all changed identities before owner execution.
- Owner runs PRE -> 27 git mv -> overlay -> POST -> 79-test Windows suite and
  import checks -> exact stage -> local commit -> COMMITTED PASS -> push.
- Stop on any failure. Never enable termination, scoring, real mode, holdout,
  orphan bypass or an allowlist entry. No scientific execution is authorised.
- After GitHub push, Claude independently verifies exact commit contents.

## 4. Explicit REVIEWER-DECIDED

N1I-RD-01: Retain HIGH tier and mandatory RECHECK for the always-review reader,
coordinator/receipt and identity changes. Code diff and proposed assurance plan
are acceptable at candidate scope, subject to full Windows/final-install proof.
N1I-RD-02: Identify N1I-C01 as CORRECTION requiring focused RECHECK;
COMMITTED PASS MUST precede push.
N1I-RD-03: Preserve the separate E1-ALIGN firewall repair, historical receipt
fail-closed behavior, ratified NAMES-1 limits, and owner-only installation.

No ratified scientific/safety exception is granted. Report decisions under
the indefinite owner oversight rule (Claude checks each; owner reporting by
exception). This review makes no claim of actual Windows testing or installed
code acceptance. No Git mutation or project code/test execution was performed.
