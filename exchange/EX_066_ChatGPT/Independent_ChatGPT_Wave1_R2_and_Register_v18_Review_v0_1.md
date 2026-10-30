# Independent ChatGPT Wave 1 HIGH-tier R-2 and Register v0.18 Review v0.1

Date: 2026-10-30
Project: hydra3333/analysing_perceived_randomness_in_reality
Scope: EX_065_Claude.zip, W1_Install_v1_candidate.zip, BASE_7462ea9_src_tests_template.zip,
       ratified Wave 1 design v0.1r1, register v0.18 candidate and the template draft 2.
Authority: Independent review; not owner ratification, Windows acceptance or release.

## 1. Verdicts

- Wave 1 R-2 HIGH-tier code review: PASS. 0 BLOCKER; 0 CORRECTION; 0 OPTIONAL;
  0 RECONSIDER. Reviewer decision W1-066-RD-01.
- Register v0.18 content review: PASS; no corrections. Reviewer decision REG18-066-RD-02.
- All owner-controlled acceptance gates remain applicable. Reviewer decision W1-066-RD-03.

## 2. Archive and source identity evidence

- EX_065 outer ZIP SHA-256: a2bd9edde99ae04a30532dabc65c97b9a6603199f56dec087aa115c46f2b454a.
  Eleven non-directory members; ZIP CRC verification passed.
- EX_065_Claude.md SHA-256: 7f89881fc1f91938c232f8b7b072f54eda2a9655b2581b43987df35557c75a2a.
- W1 candidate ZIP: 27c7a06fb7fd32a92a2af84535f46fd47b9f945e110715fff7246cd45a1a97ee.
  Ninety-one listed file members; all raw and LF-normalised member hashes match the
  supplied W1_Install_v1_zip_members.txt; ZIP CRC verification passed.
- BASE snapshot ZIP: 16f4b2755345c0eebcc8b418054e3aae3019b1d9cf915c0442aed490d0462bdf.
  All 293 file members match the supplied two-form hash inventory; ZIP CRC passed.
- Overlay: 88 files = 84 additions and four replacements. Its manifest lists 83
  added files and four replacements; the manifest itself is the 84th added file.
  Every manifest identity matches the overlay; every replacement predecessor hash
  matches the supplied base snapshot. No other source or test files were replaced.
- The four-file unified diff was successfully reverse-applied to the replacement
  bytes, producing the baseline bytes exactly for the runner and three template files.
- Frozen design note v0.1r1 in the overlay matches SHA-256
  06b491225812e14962aef99e299cbd6c003be68bb5a73425e566f1b1fe685060.
- The supplied snapshot was checked against its inventory, not independently fetched
  from live GitHub commit 7462ea9. Commit identity will be checked after installation.

## 3. HIGH-tier scientific/code findings

- The shared exact helper's direct and independently structured counting routes are
  coherent: newest-S counts versus prefix subtraction; direct lambda powers versus
  recursion; period-block versus draw-index assignment. Input checks reject duplicate
  or out-of-range labels. No project data/file access occurs in the helper.
- E_7 applies (c*r + k)/(c + M), with c=52 and fair marginal r=K/L; E_7's full-history
  calibration variant has E_1's ranked groups by design. The score and separate
  probability-vector fields are verified against a second calculation.
- E_8 uses the specified exact period-moment excess-variance estimate, clamps the
  pooled variance to [0,r*(1-r)], and blends the latest-period and pooled rates.
  Its exact marginal scores sum to K and remain within [0,1]. Variants may coincide
  on particular histories; the new README warning is mathematically correct.
- E_9 uses exact decayed occurrence sums for factors 5/6, 18/19 and 37/38.
  E_10 uses exact contrasts between its declared short and earlier windows.
  Both are score-only; neither fabricates a probability vector.
- The 12 variant IDs and minimum histories match the frozen design. All 24 added
  declarations (2 games x 4 methods x 3 variants) specify revision 1, correct
  probability kinds and observation view. All 24 registry entries are FORMULA_OPEN;
  all four IN_DEVELOPMENT flags are present. Registry placeholders remain installed.
- Normal dispatch refuses these unreleased variants. The contract modules do not
  read draw files, run subprocesses or use external inference libraries. The older
  coordinator, reader and released-science boundaries are not altered by this overlay.
- Review of the supplied tests covers E_8 variant overlap, separate probability
  tampering, exact sums, insufficient history, synthetic suffix invariance, and
  negative dispatch/registry conditions. No new defect was identified.

## 4. Independent tests

Offline trial assembled from the supplied BASE snapshot plus only the overlay src,
tests and template files. Python 3.13.5, Linux. No project real master was supplied.

- 8 new tests in tests.test_occurrence_counts: PASS.
- 18 new tests in tests.test_wave1_frequency: PASS.
- 231 selected predecessor tests across 16 applicable modules: PASS.
- TOTAL independently reproduced: 257 selected tests, 0 failures, 0 skips.
- Exclusions: 10 real-master-dependent tests in tests.test_multigame_reader_contracts;
  E2R-T12, the one six-worker test in tests.test_e2r_contract. They were not run.
- The package claims 268/268 on two author environments, and 29/29 planted mutations.
  Both are recorded as Claude-side evidence; the mutation suite was not independently
  completed. The template fake-method trial and four-platform install rehearsal are
  likewise author evidence, with the source and output inspected rather than rerun.
- Windows 3.15.2 acceptance and the owner T12-W1 decision are required independently.

## 5. Register v0.18 review

- Reversed the three changes encoded by make_register_v18.py directly from the
  candidate. The resulting v0.17 bytes have SHA-256
  268e72b2a435628550079682040ae2eab69b5a08baa3241e4ee9e47e54499d17,
  exactly the expected installed identity.
- Ran the supplied builder from those independently reconstructed bytes. It applied
  its three unique counted edits and reproduced the supplied v0.18 byte-for-byte.
  Canonical LF SHA-256:
  68ca2cee462e37658b088632bcc5272e0bf42ed4dbefc4fc3cb0f2b617c04580.
- The new section records H1F5-C01, the DOC-7 handover installation at 8defe9d,
  the owner's revised ordering, EX_061..064 and W1-C01, W1-1..6 and the proposed
  wave 1 installation with explicit unreleased state. It distinguishes the
  proposed Windows acceptance from completed evidence, and marks out-of-date
  statements rather than silently rewriting their historical source documents.
- "RATIFICATION CANDIDATE" and "[T12-W1]" are intentionally unresolved.
  Their owner-controlled finalisation must not silently change method science.
- No content correction is required.

## 6. Disposition and boundaries

W1-066-RD-01 (REVIEWER-DECIDED): Wave 1 R-2 HIGH-tier PASS for this exact reviewed
candidate. It authorises owner consideration, not installation or a run.

REG18-066-RD-02 (REVIEWER-DECIDED): Register v0.18 CONTENT PASS, subject to owner
ratification and accurate status/T12 finalisation.

W1-066-RD-03 (REVIEWER-DECIDED): Owner must resolve [T12-W1]. The owner Windows
268-test suite (including the T12 decision) must precede committing, with PRE,
POST and COMMITTED verification and Claude's subsequent GitHub check. The absence
of my own T12 or real-master runs is not a waiver.

No installation, real master, holdout, real development, safety-switch change,
coordinator action or scientific execution was performed in this review.
