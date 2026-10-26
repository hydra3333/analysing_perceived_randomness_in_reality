# Claude mechanical check of the ratified installation package, v1

**Reviewer:** Claude (independent reviewer)
**Date:** 26 October 2026 (Adelaide)
**Checked:** `Predictive_Randomness_Governing_Documents_v0_4_OWNER_RATIFIED_INSTALL_CLAUDE_CHECK.zip`, SHA-256 `20c883a990deb78def411b2ed3c6e7206b5964d3ca3ab9192d823a8d059bd06b`
**Against:** my approved v0.4 candidates from `ac79c963...245822`, and GitHub HEAD `c93ef81`.

## 1. Verdict

**One CORRECTION to resolve before installation.** Everything else passes.

## 2. Verified

| Check | Result |
|---|---|
| File names | All eight destination files present, with the candidate suffixes removed; every file is LF. |
| Content diff (my own, each file against its v0.4 candidate) | Only title, status, authority and "historical" wording changed, except the one item in section 3. |
| Installed hashes | The seven document SHA-256 values in register v0.3 match the package bytes. The register's own SHA (`b8704c2d...0a9a`) is in the package evidence, not self-referenced. |
| 17 historical register identities | All 17 hashes are unchanged from register v0.2 and match the files at HEAD `c93ef81`. Only their status words changed ("Current" to "Historical"). |
| Protected blocks | All seven are byte-identical in the installed files: Architecture 5C; R2 section 7 and 4.1; R3 0.4, 2.4 and 3; Proposal E_1-E_6. |

## 3. CORRECTION

**R3 v0.4, line 37: the effect of ratification has changed.** The ratified R3 (v0.2/v0.3, and the v0.4 candidate) defines `[R3-PROPOSED]` as "proposed here for owner assessment and ratification", so ratifying R3 ratifies those provisions. The install edit replaces the authoring-time sentence with:

> "Items explicitly labelled R3-PROPOSED, RECOMMENDED or OPEN remain unapproved choices unless separately decided by the owner"

Read literally, this would leave most of R3 unratified even after ratification: the TOP/WORST and rank-position definitions, the freeze and publication process, and the reporting rules are all labelled R3-PROPOSED. T-39 then blocks FINAL until R3's scoring is ratified. This is not a status-only change.

**Recommended replacement (owner to confirm):**

> "Later approved owner decisions supersede earlier conflicting text. With the owner's ratification of this edition (26 October 2026), provisions labelled [R3-PROPOSED] are ratified as written; items labelled OPEN, and decision-register entries still marked OPEN, remain undecided. This ratification neither silently amends another contract nor decides the first implementation of an unresolved E-method."

If the owner instead intends R3-PROPOSED items to stay unapproved, that is a substantive decision. It should be recorded explicitly in the register, noting its effect on T-39.

## 4. OPTIONAL

- Register row for R2 v0.4: "+ proposed ERR-R2-06" should be "+ owner-decided ERR-R2-06". The date also sits mid-sentence ("pending Windows gates 26 Oct 2026"), and the P3 row has the same placement.

## 5. After the fix

Re-issue the package with the R3 line corrected and the register's R3 hash updated. Claude re-checks that single diff. Then the owner commits and pushes, and Claude verifies the committed hashes at the new HEAD.

*End of document.*
