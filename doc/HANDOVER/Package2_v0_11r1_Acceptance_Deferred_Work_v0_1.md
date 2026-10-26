# Package 2 v0.11-r1 — owner acceptance, installation and deferred tests v0.1

**Date:** 27 October 2026 (Adelaide).
**Work item:** P2-V011R1-INSTALL — factual checkpoint, **NON-NORMATIVE**.
**Author chat:** ChatGPT Package 2 coding conversation (existing primary coder).
**Independent reviewer chat:** new Claude chat (current roles).
**Source base:** `618fe48c48ada46bcf60c80bbd291acc216d7e3b`.
**Status recorded:** owner agreed to accept the independently reviewed v0.11-r1 offline implementation and the consolidated owner-applied installation overlay; repository installation/commit remains to be performed and verified. This record must not be represented as Git installation evidence before the owner's commit is verified.

## Accepted Package 2 code

- Review parent ZIP: `Predictive_Randomness_MultiGame_Package2_v0_11_CLAUDE_REVIEW_ONLY.zip`, SHA-256 `0e00e231c46dafd01df52fb6f50db6ceaf399ea27be40efb318529101611d74c`.
- Focused r1 ZIP: `Predictive_Randomness_MultiGame_Package2_v0_11r1_FOCUSED_CLAUDE_REVIEW.zip`, SHA-256 `7bddda746f56668fbc60af9826cee83c7fd95031dfd3c9b4b474641cc2734635`.
- Independent review ZIP: `Claude_Review_Package2_v0_11r1_v1.zip`, SHA-256 `5c2e84655dcfd1d3a24129c0d38a5996e2f14195e807def382ba2bdb7d545a29`. PASS: **0 BLOCKER, 0 CORRECTION, 3 OPTIONAL**. Claude independently reproduced the reviewed test suite and performed 96/96 N−1 suffix-isolation comparisons.
- Installation consists of the 26 original v0.11 overlay files with **exactly two r1 replacements**, plus this factual, non-normative repository checkpoint under doc/HANDOVER/. The 26-source-file hashes are preserved in the installation package's `EXPECTED_SOURCE_SHA256.json`, and in Claude's original installation inventory. No other source files, ratified documents or masters are changed.
- Current safety switches remain `False`; the scientific-result allowlist remains empty. No Windows, lifecycle, destructive, scientific, ranking, master update, holdout, Mode H, FINAL or enabling-gate operation is authorised by acceptance or installation.

## Deferred optional test hardening (must remain visible)

**P2-R1-O1 — T-05 expanded fixture coverage.** Add an intermediate-target `N` and an *equal-length* suffix-perturbation case to the automated N−1/DrawView regression suite, comparing every method-visible field, array byte, schema and digest. Claude's independent 96-view probe already passed; this is regression hardening, not a current blocker. **Disposition: DEFERRED/APPROVED FOR SCHEDULING, not implemented.** Proposed slot: the first separately scoped post-install offline test-hardening package, preferably before the next consequential reader/view extension for E_2-readiness. This is a convenient scheduling recommendation, **not an additional mandatory E_2 gate**. The owner authorises that scoped work separately; roles/review apply as of that time.

**P2-R1-O3 — Protected-coordinator AST baseline fixture.** Make the existing AST regression reliably obtain the committed v0.6 coordinator baseline when run from an independently reconstructed test tree; it must no longer skip merely for a missing baseline-path parameter. It must compare all eleven protected functions. Claude already independently checked 11/11; this is test-harness hardening. **Disposition: DEFERRED/APPROVED FOR SCHEDULING, not implemented.** Schedule alongside P2-R1-O1 in the same future bounded test-only package, with independent review.

**P2-R1-O2 — Consolidated installation transport.** Owner agreed: install the single, exact reviewed 26-file combination using an exact source-file overlay and SHA-256 verification. Satisfied by the present installation candidate when its post-install verification passes.

Other open, previously classified **OPTIONAL / TO-TEST** items continue: resolved-path containment under `source_data`; NTFS `st_nlink` behaviour on the owner's Windows installation; full review of `multigame_windows_lifecycle_v1.py` before any lifecycle gate. They are **not** silently closed by v0.11-r1.

## AI role transition remains separately gated

The ratified AI roles agreement v0.1r1 provides **ADD-2** (current ChatGPT coder transfer), **D-1** (earlier Claude reviewer delta), then reviewed and jointly installed **H-1/H-2/H-3**. The owner must designate its effective commit/milestone. An installation of Package 2 code **alone does not activate the changeover**: until the whole ratified transition is installed, current working roles continue (ChatGPT coder, Claude reviewer). The project owner remains sole committer and run authoriser.

## Evidence/status distinctions

`IMPLEMENTED` and `REVIEWED` are supported by the supplied reviewer archives. `ACCEPTED` is the owner's 27 October agreement for the reviewed offline code. `COMMITTED` and the new Git HEAD must be separately verified after installation. No source-/outcome-bearing file or science ledger is part of this package.

**Role-switch scheduling recommendation:** the owner should expressly name a later effective transition commit (not infer one from the Package 2 code acceptance commit), after ADD-2 and D-1 are exchanged and H-1/H-2/H-3 are reviewed and ready for atomic owner-ratified installation; preferably before E_2-readiness implementation. This recommendation does not itself designate that commit.
