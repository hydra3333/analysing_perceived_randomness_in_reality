# Independent ChatGPT HIGH-tier E1-ALIGN code RECHECK v0.1

Date: 2026-10-28
Project: hydra3333/analysing_perceived_randomness_in_reality
Scope: EX_027_Claude.zip plus E1ALIGN_Code_Install_v1.zip; static and packaging review only.

## Verdict

PASS at independent code-review / candidate-package stage.
0 BLOCKER / 0 CORRECTION / 0 OPTIONAL / 0 RECONSIDER.
This is NOT Windows acceptance, installation authorisation, an installed-code claim, or a release approval. The owner must ratify register v0.10, authorise the final exact package, run the Windows gates, and commit/push only after COMMITTED PASS. Claude must subsequently verify GitHub.

## Identity and file coverage

EX_027_Claude.zip SHA-256: 9a9fc2d7c90c39f636f5b0876ff6d41ab271d243a4382ac7c2e6ec40d15e7b25.
E1ALIGN_Code_Install_v1.zip SHA-256: c613cc1af2a5ec89baf2d37bce6101c38469cd3b361b2b092270938dd5e7b00c.
Both ZIP CRC checks pass; EX has 14 files; installation ZIP has 27 regular files (plus directory entries).
Its overlay comprises 21 tracked new/modified file paths plus the unchanged file moved through git mv. The SHA-256 manifest has 20 entries excluding itself; all 20 match. The verifier's 21 expected SHA-256 values also match the overlay, including the manifest's own SHA-256.
Frozen allowlist SHA-256: aaf7f46e529ff42036cf7f943c4efc6232edbd2c3ff463e9e1be02f10a975164.
Five moves, 10 edited files, 22 counted edit blocks, three added code files, and one unchanged move. The 14-path Git trial diff was reversibly applied in an isolated scratch tree (using an explicitly marked placeholder only for the unchanged moved standalone contract), then reapplied to reproduce the overlay. All ten edited files independently reconstructed from the inverse-patch predecessor text plus the allowlist and matched the supplied exact new bytes. All three added code SHA-256 identities match.
Nine of the ten inverse-patch predecessor files were also compared to the corresponding bytes in the earlier reviewed NAMES1_Code_Install_v1.zip overlay, with exact matches. The tenth, E_1 core, was verified against the supplied reversible diff and frozen allowlist, not a separately fetched Git commit.
Both extracted function bodies, canonical_bytes and length32_tuple (formerly _length32_tuple), are AST-equivalent to their original definitions. Their non-identity-changing scientific bodies are unchanged. All supplied overlay Python sources parse successfully.

## Verifier and install route

Read VERIFY_E1ALIGN_INSTALL.py, RUN_E1ALIGN_SUITE.py, CHECK_E1ALIGN_IMPORTS.py, RENAME_FILES.cmd, STAGE_EXACT_FILES.cmd, and INSTALL_INSTRUCTIONS.md.
- PRE requires a clean worktree, ancestry from b64c2a6, identical HEAD src/ and tests/ trees, eight guarded hashes unchanged, and new paths absent.
- POST requires precisely the five staged moves with base blobs, ten allowlisted worktree edits, eleven untracked new files, each reconstructed source matching its base-plus-allowlist, the unchanged moved file matching its base, and old paths absent.
- COMMITTED requires a clean tree, one parent whose src/ and tests/ remain unchanged since the base, exactly 5 deletions, 5 moved-path additions, 11 other additions and 6 in-place modifications, with all Git blobs matching.
- All verifier Git calls use --no-optional-locks with GIT_OPTIONAL_LOCKS=0. Its committed STOP emits identities and forbids push or reset. Commit verification precedes push.
- The Windows runner requires 84 expected tests in ten modules, with only specified symlink skips allowed. The fresh-interpreter checker verifies five old/new module origins, shared encoder object identity, reader independence, then control plus mutations m1..m18 (37 checks).
- The reader firewall guard enumerates exact E_1 import and textual allowances; newly added method modules are scanned. Import-symbol bypasses identified in earlier reviews are covered by negative tests.

Claude's provided Linux evidence: all 84 tests passed (zero skips) under Python 3.13.17 and 3.15.0b4. The 25 design checks and 37 fresh-interpreter/import checks show PASS, and the disposable-clone install and rollback logs report the stated outcomes. Those logs were inspected as author-side evidence, not independently reproduced on Windows.

## Limits and required owner gates

A live GitHub copy of commit b64c2a6 was not independently fetched in this review; that identity is deliberately checked by PRE/POST/COMMITTED on the owner's actual checkout. No project module was imported and no project tests, real science, holdout, process-control or installation code was run by this reviewer. Static comparisons, a scratch Git patch round trip, and the document builder were used only offline.
The owner must explicitly check each command's PASS before advancing; CMD blocks do not automatically stop the next pasted command on a prior failure. The mandatory fresh-process import checks, 84-test Windows acceptance on the current owner-approved interpreter (Python 3.15.2), permitted Windows skips only, guarded identities and all three verifier phases remain open. PRE, POST or tests failing means STOP before commit. COMMITTED failing means STOP before push; no reset or process-kill workaround.

## Conclusion

Independent HIGH-tier candidate review PASS. The E_1 revision-1 structural exception remains conditional on the owner's Windows evidence and exact installation acceptance. Nothing enables switches, scientific coordination or result promotion. Any unexpected final-source or allowlist change requires focused code RECHECK.
