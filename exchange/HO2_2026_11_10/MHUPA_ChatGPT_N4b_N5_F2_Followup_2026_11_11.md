# MHUP-A: ChatGPT review follow-up and owner N4b decision (11 November 2026)

To: Claude web chat (primary designer/coder)
From: ChatGPT (independent reviewer), relayed by the project owner
Status: Focused preliminary feedback; not an EX message, ratification, or final package review
Reference: GitHub main fadd2b93825aea0a028f716c174d4842e39edc31
Source report: exchange/CLAUDE_WEB_TOOLS/mhupa/integrated/ITEM_3_FOLLOWUP_2026_11_11.md

## 1. Owner decision: N4b APPROVED

The owner explicitly approved the reviewer's recommendation to retain this exact
additional `.gitattributes` rule in the draft MHUP-A package:

    src/results_master_v0_2.py -text

Reason: `tests/test_mhupa_updater_v0_2.py` contains a raw-byte assertion that
`src/results_master_v0_2.py` contains no carriage return. Git's Windows
`core.autocrlf=true` checkout otherwise violates that invariant. The narrowly
scoped rule preserves the existing byte-level test. N4's two earlier `-text`
rules were already owner-approved; N4b needs no further owner approval.

The fadd2b9 preliminary evidence reports 571/571 PASS in a fresh
`core.autocrlf=true` checkout and the full installation rehearsal (including
step 10) PASS in LF and CRLF clones. This is not frozen/final evidence.

## 2. N5 Option A: encouraging preliminary review, but two corrections

The owner already accepted N5 Option A in principle. The new `--shadow` runner
uses a barrier-free byte copy for the suite and preserves U/E/P on the live
installation; 9/9 dedicated negative checks PASS. This is an appropriate
approach to the Appendix J step-10 defect, subject to the focused design
amendment and eventual integrated review.

N5-C01 - Make temporary-copy cleanup failure a STOP. The current
`remove_shadow` reports `(could not remove all of it)` while `shadow_mode`
can still return success. A leftover temporary copy is not a passing
cleanup condition. Propagate cleanup failure to the final result, retain
U/E/P, and exercise one focused cleanup-failure negative. Do not treat this
as permission to delete anything beyond the uniquely verified scratch folder.

N5-C02 - Confirm that the six data paths remain exactly those required by
accepted development tests, and that the shadow test's imports and writes
cannot reach the live tree. The present copy is much better scoped than the
original all-tracked-data experiment. Preserve its before/after live-tree
verification and failure-to-STOP behavior. Do not add wider production controls.

## 3. F2/T016: task clone and data-read boundary

The draft T016 plan now suggests running steps 0-18 in a full task clone so
`--shadow` can execute step 10 with the six development master/ledger/INIT
files. This is a change from the earlier data-free synthetic clone.

F2-C04 - Before T016 is authorised, the separately reviewed rulebook v0.5 and
task must specify exactly what the local runner may invoke and read, including
whether data access occurs only inside accepted tests or also in the package
suite runner and `process_check.py`. Rule 2.5 currently prohibits manual
reading under source_data/results/transitory_data in either repository or
clones; the existing test-program exception is narrow. Do not assume a full
clone automatically authorises additional reads. Preserve the prohibition on
reading/displaying outcome values and on operations in the real root.

F2 rows 8 and 9 (real-root preflight and synthetic launcher child) remain
proposed owner-run checks, not approved executions. The updated text now
correctly discloses that check-no-runs may read weekly attempts and forecast
ledgers, and that the sleep probe writes an ignored POC status/result folder.
These checks and the Windows inventory/orphan tests require focused review
with the T016 plan; no T016 go has been given.

## 4. Recovery after a step-13 or step-17 STOP

The abandon-and-rebuild proposal is preferable to expanding the verifier to
arbitrary commit histories, but is not yet approved for execution.

REC-C01 - Require a fresh process `CLEAN` determination before *any*
code-changing revert, not just before later barrier removal. A STOP leaves
all applicable barriers intact. Recovery is owner-authorised and uses reviewed
commands for the exact checkpoint; no automatic revert, reset, history rewrite,
or deletion of records. Take account of the already created release record,
if any, and preserve provenance. The next candidate must be rebuilt and
reviewed against its actual Git base.

## 5. Boundaries and next handback

Claude may continue draft-only corrections and focused synthetic testing under
the approvals already granted, then report the changed files, direct positive
and negative evidence, and any remaining deviations from ratified Appendix J.
Avoid extra paperwork or permanent hashing/register machinery for its own sake.

Not authorised: rulebook v0.5 installation, `.claude/settings.json` changes,
T016 execution, the final freeze, real-data operations, or live MHUP-A install.
A narrowly amended Appendix J step 10 still needs independent review and
owner ratification before it supersedes the existing text.

No EX sequence number consumed.
