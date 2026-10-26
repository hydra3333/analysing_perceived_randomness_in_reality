# Claude spot-check of the consolidated governing documents v0.4, v1

**Reviewer:** Claude (independent reviewer)
**Date:** 26 October 2026 (Adelaide)
**Reviewed:** `Predictive_Randomness_Governing_Documents_CONSOLIDATED_v0_4_CLAUDE_SPOTCHECK.zip`, SHA-256 `ac79c963aec3d1e659b6ccc0a43fc90188e7003aa51cff3a6587899acd245822`
**Baseline:** GitHub HEAD `c93ef81`. Its `doc/`, `source_data/` and `src/` are unchanged since `cf00999`.
**Method:**
- My own diff of each v0.4 file against my copy of the v0.3 candidates. The v0.3-to-v0.4 changes are confined to Proposal, R2, R3, Architecture and the register; P3, the exposure record and the numerical reference are byte-identical to v0.3.
- My own ID inventory against the ratified sources.
- Protected-block extraction from the ratified files.
- A stale-phrase comparison of v0.3 against v0.4.
- The package verifier (PASS).

**Status:** review only. No winning, Powerball or supplementary numbers appear in this document.

## 1. Verdict

**PASS. No BLOCKERS and no CORRECTIONS. The consolidated v0.4 candidate set is ready for owner ratification.**

## 2. Verified

| Item | Result |
|---|---|
| B1.1 date rule | R2 section 3.1A: the derived weekly date formula; a value-free discrepancy warning; a game-local halt of E_14, E_54 and equivalents pending owner decision; unrelated `UNORDERED_SET` methods not blocked; no permission for any N-1 loader to decode row N or later. Cross-referenced in R3 (after section 1.5). Matches ratified 0A.3 and ERR-R2-05. |
| B1.2 new-view binding | R2 after R2-C09: every new schema in either game binds game_id, era and profile; `E1_REAL_U_TRAINING_VIEW_V1` is the sole legacy exception and stays byte-identical; the master SHA is never a view digest or seed. |
| B1.3 per-game status | R2 status paragraph plus the R2-C13 multi-game extension: SUPPORTED / FORMULA_OPEN / UNSUPPORTED_FOR_GAME with a structural reason. Placed outside protected section 7 (which remains byte-identical). Clearly distinguished from the lifecycle vocabulary. |
| B1.4 identity | R2 section 2: the `(game_id, draw_number)` pair; `draw_key` display-only; a versioned legacy rule; separate namespaces. |
| B1.5 OPEN / no authorisation | R2 section 13.5: every ERR-R2-05 OPEN item, including walk-forward 1145-1576 / 1475-1693, and a no-authorisation clause that covers Oz execution, frozen results, quarantine access, destructive tests, switches, Mode H, FINAL and the interlock. |
| B1.6 method-generic | Architecture section 20A: a mandatory contract before E_2, explicitly not satisfied by the P3 entry alone. |
| C1-C5, C7, C8 | All applied exactly as requested. |
| C6 | The R2 section 0.3 change-control rules are restored verbatim. The binding philosophy quote is verbatim (checked against the ratified line). |
| C9 | The Architecture 5A.2 numbered requirements 1-7 are restored. The default is INSTALL + UPGRADE. Item 6 adds the post-upgrade STOP (offline, boundary, N-1, W-01..W-25 including W-23, E_1 goldens), no implicit upgrade on invocation, and no upgrade between freeze and score or within Mode H. |
| Optional O1 | The "Important distinction" note is restored. |
| Protected blocks | Architecture 5C (all of it), R2 section 7 and R2 4.1 are byte-identical to the ratified text (my own extraction). |
| IDs | None missing. The R2 count is 107 distinct I-/R2-C/R2-D/T- IDs, which confirms the package's metadata note; my earlier 108 also counted the token "N-1" as an ID. A-1/A-2 were revision-history labels whose substance is in 5A.1, W-04 and W-19. |
| New authority / weakened rules | None found. Every addition is a restoration of ratified substance or an owner decision. The holdout, N-1 and process-safety text is unchanged or strengthened. |
| Stale phrases | The only new hits are in restored or corrected text, with correct meaning (for example "former 12-worker condition withdrawn"). |

## 3. OPTIONAL (does not block ratification)

- **O1:** Architecture 5A.2 item 5 says "once-only opening of the original ten-draw holdout". Consider "the once-only Mode H opening of each game's FINAL_HOLDOUT_10".

## 4. Next steps

1. **Owner ratification** in this order: Proposal v0.5; then R2 v0.4 and R3 v0.4; then Architecture v0.7 and P3 v0.2; then the exposure record and the numerical technical reference; then register v0.3.
2. **Installation ZIP.** Claude mechanically compares it with these candidates. Only the status lines, the candidate suffixes in file names and the register hashes may differ.
3. **Commit and push**, then Claude verifies the installed hashes at the new HEAD.
4. **Claude reviewer handover v9**, then **Claude review of the definitive ChatGPT coder handover** (five areas, with a two-way comparison).

*End of document.*
