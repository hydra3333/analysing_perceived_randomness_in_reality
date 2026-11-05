# EX_148 evidence supplement - ChatGPT artifact verification (not a new exchange number)

Date: 2026-11-05
Project: hydra3333/analysing_perceived_randomness_in_reality
Subject: EX_147 binary attachments supplied after EX_148 - evidence audit
Status: Supplemental audit only. EX_148 R-2 HIGH RECHECK remains in force.

## 1. Verified artifacts

The owner subsequently attached EX_147_Claude.zip directly to this conversation.
Its SHA-256 is:
  a5ac750f5699b3a5f99bfda6d5b67f3aa85a6754ccaecef7a61f8cbb26d1ef25
This matches the announced outer archive digest.

The nested MHUPA_Slice2_Review_v1.zip SHA-256 is:
  94fd6c0751dcd46c724d27d95031dcb5d0207727fb7c2ac279e03ef24aa2db96
This matches the announced nested archive digest.

All six non-directory members of the outer ZIP were read successfully; their
stored digests agree with the listed digests in EX_147. The nested members
list covers exactly 127 regular files; there are no unlisted extra files or
missing listed files. All 127 stored SHA-256 hashes MATCH. All 127
CRLF-to-LF-normalized SHA-256 hashes MATCH as well (three files differ on
normalization). The nested ZIP also contains directory entries, which are
not listed as regular members.

The package contains the reviewed overlay code, tests, mutation script,
source diffs, and the three stated test/mutation evidence logs.

## 2. Evidence in the archives (inspected, not independently executed)

- Python 3.13 suite log: total ran 561, expected 561, skips 0, SUITE PASS.
- Python 3.15.0b4 suite log: total ran 561, expected 561, skips 0, SUITE PASS.
- Python 3.13 mutation log: 85 mutants, 76 caught, 9 marked EQUIVALENT
  with explanations, 0 unexplained survivors. Its baseline reports passing.

These statements describe the supplied log contents. No project tests,
mutation scripts, lottery results or holdout operations were run for this
audit. This audit does not independently verify the separate owner Windows
T018 report, which is referenced but not included in this ZIP.

One relevant qualification: mutant [55] is labelled EQUIVALENT in the
supplied log expressly because the current test does not plant a foreign
score-ledger line. That is *test non-detection*, not proof of semantic
equivalence. It reinforces EX_148 B04's request for malformed, duplicate,
missing, extra and mismatched score-ledger negative oracles. A zero-survivor
summary must not be taken to resolve those review findings.

## 3. Cross-check with EX_148

I inspected the actual packaged source in:
- overlay/src/evaluation/mode_h.py
- overlay/src/evaluation/report.py
- overlay/src/evaluation/report_writer.py
- overlay/src/package_tools/install_records.py

The packaged code confirms the substance of EX_148's four blockers:
B01: Mode H score records are published as one complete create-only ledger;
B02: the report still uses sequential create-only txt/csv/json files, without
      per-file resume after a partial report;
B03: released_variants() subtracts explicit retirees/superseded_by but
      does not implement the claimed current-registry-chain supersession check;
B04: an already-existing ledger can pass _ledger_lines() and reach
      SCORE_COMPLETE before exact complete roster/score/rank coverage is
      checked by rebuild_from_ledgers().

The original EX_148 discussion of the thirteen interpretations and the
additional design dispositions remains unchanged. The independent source
findings are not resolved by the integrity of the ZIP or by passing tests.

## 4. Disposition

EX_148 remains R-2 HIGH RECHECK. The earlier inability to validate the
binary artifacts is now RESOLVED for archive integrity and inspection of
provided evidence. It was a limit of the earlier review, not a defect in
Claude's package. There is no new exchange number in this supplemental note.

No installation, real-data operation, results update, holdout opening or
scientific run is authorised by this audit.

End of supplement.
