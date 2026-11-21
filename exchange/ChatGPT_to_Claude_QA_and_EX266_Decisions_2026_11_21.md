# ChatGPT reviewer handback to Claude — QA reset, PROD copies, and decisions for EX_266

**Date:** 21 November 2026 (Australia/Adelaide)  
**Project:** `hydra3333/analysing_perceived_randomness_in_reality`  
**Author:** ChatGPT, independent reviewer (accepted under HO-2)  
**Status:** **Owner-discussion handback; NOT an EX; NOT a ratified design; NO permission to implement, install, copy, wipe, back up, restore, fetch results, or run software.**  
**Repository sources consulted:** `main` at `51c3fa8`, decision log through entry 134, EX_264, EX_265, both draft designs and Claude's contradictions analysis. **The owner's new decisions below came later, in this reviewer chat, and are not yet in the repository decision log.**

## 0. Instructions for interpreting this handback

The owner wants Claude and ChatGPT aligned before Claude prepares **EX_266**, the corrected **complete system specification and deployment design**. The owner has substantial hands-on DEV/QA experience and wants a useful independent QA laboratory, scientific correctness and recovery, **with as little administration and over-engineered software as practical**.

Labels used below:

- **OWNER — NEW:** explicitly stated by the owner in this reviewer chat after decision log entry 134.
- **OWNER — EXISTING:** previously recorded decision, sometimes reaffirmed here.
- **REVIEWER ADVICE:** a suggestion, **not** an owner decision or ratified mechanism.
- **DESIGN TO RESOLVE:** engineering for Claude to propose and the reviewer/owner to evaluate; do not claim that the owner chose its implementation.

Where the unratified specification v0.3 or deployment design v0.9 contradicts a later owner decision, **the later decision prevails**. Preserve earlier formal authority until ratification of the replacement. Do not silently turn a suggestion into an owner choice or re-open an already settled policy.

## 1. Reframe QA accurately

**OWNER — NEW:** QA is an **independently managed experimental/test environment**, **not** a continuously synchronized replica of PROD and **not** a gate for installing to PROD. Several normal scenarios are legitimate:

1. QA has **exactly PROD's installed software and scientific controls** as a clean comparison baseline.
2. QA has that software plus **new variants or experimental infrastructure** being investigated.
3. QA deliberately has **more or fewer variants** than PROD.
4. QA differs from PROD's infrastructure during a test and, when the owner chooses, is returned to a PROD-equivalent baseline.

QA is sometimes an unruly laboratory. The ability to **wipe and replace its installed software to return to PROD's known software state** is a *real need*, not a hypothetical convenience. It is an owner-initiated reset, not a requirement to keep QA continuously matching PROD.

**OWNER — EXISTING:** DEV, QA and PROD each have their **own `ENVIRONMENT.ini` at their own root**, defining role, root, Python `.venv` location, backup root and relevant paths. DEV's configuration also names QA/PROD locations. Configured examples are DEV on E:, QA on D:, PROD on G:, PROD backups on T:; never hard-code these paths. QA's local INI controls QA, not PROD. Each tree has its own Python environment, backups and operational state. Preserve role validation, process safety, source and results restrictions. QA must never contact a lottery website. No DEV/QA-to-PROD output flow is inferred.

**OWNER — EXISTING, entry 126:** **QA is NOT required for PROD installation.** PROD can install directly from ready DEV material, subject to the target's own checks. No mandatory QA certificate or QA/PROD matching test. This is unchanged by the new ability to reset QA from PROD.

### Two distinct PROD-to-destination operations, which must never be conflated

**(A) Reset/copy installed SOFTWARE from PROD into QA:** **new capability decided here**; target is only **QA**.  
**(B) Reseed complete RESEARCH DATA from PROD into QA or DEV:** **previously decided**, reaffirmed here.

The owner may run either separately or deliberately run both. **A must not automatically invoke B; B must not automatically invoke A.** A further **(C) reset/replay derived research data in a deliberately chosen tree** is a third, separate tool/operation, not a side effect of A or B.

## 2. (A) Install/reset QA SOFTWARE from PROD — NEW REQUIREMENT

**OWNER — NEW:** The owner envisages a small tool, perhaps `INSTALL_FROM_PROD` into QA (illustrative name only), which safely reproduces PROD's *currently installed software state* in QA, using a **wipe-and-replace** approach for the relevant QA software. The owner considered manually removing QA and copying PROD's entire folder to QA, editing its `ENVIRONMENT.ini`, but recognises that blind whole-tree copying is unsafe.

**Intended semantics:**

- The owner selects this **explicitly**, when wanting QA's installed software back to PROD's state. Unlike ordinary add-only installation, this **QA-specific destructive reset** may remove experimental QA variants/infrastructure and replace them with the variants, helpers, common code, infrastructure and relevant scientific/safety controls **actually installed in PROD**.
- The source PROD must be **strictly read-only**. No source-side log, lock, marker, snapshot-due file or other write; no PROD updater or job launched.
- **Preserve QA's own `ENVIRONMENT.ini`, its `.venv`, role, root, backup location and QA-specific identity.** Do not blindly transplant PROD's INI, `.venv`, live locks, process/restore barriers, recovery kits, backup history or operational records.
- **DESIGN TO RESOLVE:** Reconcile/recreate QA's **local installed-software inventory, verification markers and installation/control state** from the installed content. Copying PROD's bookkeeping verbatim cannot certify QA's own runtime or role.
- **DESIGN TO RESOLVE:** Keeping QA's `.venv` is deliberate, but copied PROD software may be incompatible with it. Verify imports/interfaces and appropriate tests using **QA's own Python**. If not compatible, fail closed for QA research and give the owner a clear route to rebuild/reverify QA's environment; do **not** copy PROD's `.venv` or assume byte-identical results across different Python/dependency versions.
- **DESIGN TO RESOLVE:** An interrupted or failed reset must not leave QA appearing operational with a half-replaced installed software tree. A simple visible barrier and recoverable retry/rebuild path are acceptable; do not build a complex release administration system.
- **Do NOT copy research data in this software operation**. Software-only reset could make QA's pre-existing forecasts, scores, withdrawal state and OV-1 incompatible with its new installed variants; warn and keep incompatible QA research from being incorrectly processed until the owner **separately** reseeds or resets/replays it. Software equality does not imply total research-state equality.
- **REVIEWER ADVICE:** A small, deliberate `Reset_QA_Software_From_PROD`-type operation appears more reliable than requiring DEV to reproduce installed PROD variants that may no longer exist in ready form in DEV. Reuse the existing installer checks where appropriate without inventing a second generalized deployment framework. A clear destructive scope and owner confirmation are advisable; precise command and transaction design remain open.

The owner's preference is **wipe relevant QA software and replace**, not a permanent file-by-file merge/diff/reconciliation bureaucracy. The exact protected/replaced file sets and crash-safe method require Claude's technical design and the reviewer's scrutiny.

**Explicitly not decided:** A generic PROD-to-DEV program-copy tool; a universal clone of every PROD byte; overwriting QA's environment, local settings or research data as a hidden side effect; using QA as a PROD installation gate.

## 3. (B) Complete PROD RESEARCH-DATA reseed into QA or DEV — ALREADY DECIDED

**OWNER — EXISTING, EX_265 §1; entry 128; entry 129:** A manual, **complete** copy of PROD research records, into **QA or DEV**, replacing the destination's active research data on the owner's command. Includes accepted draw masters and provenance, forecasts (including complete rankings/TOP/WORST), scores, cumulative leagues, other reports, both prevailing and exploratory OV-1 information and necessary scientific provenance. It must **not** copy program code, `.venv`, `ENVIRONMENT.ini`, installer manifests, locks, settings or unrelated control records. **PROD may only be read, never written**, even on failure or interruption. No Git/GitHub dependency.

**OWNER — NEW:** This is a **required capability** of the design, not an "optional feature" Claude may decide not to implement. **Invoking it is still optional/manual.** Remove the proposed separate passive-export mode; the owner does not need it.

The owner **prefers wipe-and-replace of destination active research data** (no automatic permanent reference/import directory, administrative archive of QA experiments or mandatory backup of disposable QA results). A short temporary destination-local staging/check step may be used to avoid an unusable half-copy. A busy destination must refuse; coherence of PROD during the read must be checked **read-only**, without locking or writing PROD.

**OWNER — EXISTING, entry 129:** When copied PROD results belong to variants **not installed locally** or **with different locally installed bytes**, the behaviour is **warn, ignore, continue** for local research processing. Do not let incompatible data masquerade as QA/DEV-computed results. **OWNER — NEW:** If safely achieving this behaviour takes complex machinery, the owner may reconsider the implementation; explain cost rather than silently building an elaborate new registry or archive.

**DESIGN TO RESOLVE:** The copied-list path may collide with local variant lists of identical names but different fingerprints. Claude should propose the **smallest safe** collision/provenance rule that allows a complete direct copy, leaves the source unmodified and prevents incorrect use or double-counting. No mandatory permanent import/reference tree.

## 4. (C) Explicit QA/DEV reset/replay of derived research — REAFFIRMED

**OWNER — EXISTING, EX_265 §6:** One small, owner-initiated reset/replay facility for selected DEV/QA tree: entire derived history for one/both games, or a game's draw suffix starting J with an optional endpoint N. Preserve original accepted draw masters and source/version provenance. Do not implicitly reset PROD when copying from it. A separately explicit PROD reset would need its own authorisation/scoping and is not approved now.

**OWNER — NEW, emphasis:** Reset/replay must reconstruct **ALL scientifically dependent material consistently**: canonical scores, cumulative leagues/rankings, reports, pending predictions, prevailing OV-1 and exploratory OV-1. No inconsistent downstream state treated as complete. If stopping at N requires truncating later results and doing catch-up later, say so truthfully. One clear confirmation; no nightly/ambient destructive rule.

A recalculated retrospective QA/DEV trajectory is **sandbox research**, not original prospective evidence. Sandbox labelling alone does **not** fix incorrect cumulative mathematics or cohort membership. Minimal implementation is wanted.

## 5. Explain and rename `FORWARD_FROM`, without losing the scientific boundary

**OWNER — NEW:** The owner objects to the meaningless field name `FORWARD_FROM`, because it gives no indication of **what it controls**. Prefer a descriptive name such as **`PREVAILING_OV1_FIRST_ELIGIBLE_DRAW`** (reviewer example; exact name is a design detail).

**What it actually means:** The first draw at which a *particular variant* may contribute to the **prevailing/prospective OV-1**. This does **not** prevent historical N-1 forecasts being computed and descriptively scored or used in **exploratory OV-1**.

**OWNER — EXISTING choice B, entry 130:** In PROD the boundary is defined by **the first draw not among the accepted results after a successful official-source check**, avoiding retroactive admission of a newly installed method to a draw whose outcome was already available. It is an objective draw-number eligibility rule, **not** proof that the real-world drawing had not yet occurred. Keep the conditional scientific qualification of the prevailing OV-1 error bound.

**OWNER — NEW:** DEV and QA get data through the owner-triggered copy from PROD and subsequent **manual local catch-up**. The owner **does not want extra prospective-boundary ceremony in QA or DEV**. Copied PROD data may retain its original PROD boundary and provenance; QA/DEV recomputations are sandbox and must not claim to be original formal prospective evidence. Claude must explain plainly which minimal markers, if any, are necessary for scientifically correct local replay, rather than adding bureaucracy under the old generic `FORWARD_FROM` name.

## 6. R5-F04: owner deliberately CHANGES earlier backup-gating decision

**OWNER — NEW; EXPRESS OVERRIDE of the previous agreed/recommended refusal approach:** A destructive **infrastructure overwrite** may proceed **without any programmatic check that backups exist or have been verified**. The tool must first display a **prominent warning** asking the owner to **ensure that a valid backup exists**, and demand explicit confirmation. **Default answer is NO — do not proceed.** An explicit YES permits proceeding despite an absent/invalid backup (the risk is the owner's deliberate choice).

The warning must cover:

- The overwrite could fail and require a **manual entire-tree restore** from any previously retained backup the owner chooses; no silent or automatic rollback.
- Restoring an older backup reinstates **exactly** the older software, variants, withdrawal/data state, results and `.venv` from that snapshot; later releases/withdrawals/upgrades are **not automatically installed again**. The owner can run the normal results update and chronological catch-up with that restored variant set.
- **Python version, `.venv`, dependencies and environment changes may affect runtime usability or scientific equivalence.** Do not promise identical new results in an environment that differs; the user specifically requested that caveat in the warning.
- If the owner has no valid restorable backup, recovery may not be possible. **This is an informed operator risk decision**, not an invisible bypass.

**REVIEWER ADVICE:** Keep ordinary existing best-effort snapshot routines if separately desired, but **do not reintroduce backup inventory/verification or a fresh-backup condition as a hidden prerequisite for this overwrite**. Explain honestly if a backup attempt failed; never claim a non-existent `PRE_INFRA` recovery point exists. Keep normal process/orphan safety, installable marker checks, scientific-impact checks and install-failure barriers. The general rule that research jobs can continue with backup warnings remains.

Claude must update decision log entry 128's prior assertion (and EX_265's older recommendation) with this **later owner override**, without erasing the historical record.

## 7. Settled background: do not inadvertently undo it

- **Choice A (entry 130):** Routine PROD research job invokes only the reviewed Lotterywest-GOV updater via its own launcher, unless the owner selects `--no-update`. QA and DEV do not contact lottery sites.
- **Choice C (entry 131 superseding 130):** Before phase 1 moves sources, owner himself makes a **full ZIP of the local E: project folder**, including ignored research/run records and `.git`. No `Cold_Copy` script, no second required GitHub ZIP. To inspect old system restore ZIP in a **new folder**, not atop active DEV.
- **Choice D (entry 130):** Owner explicitly withdraws a defective variant via one `WITHDRAWN_FROM` record and confirmation; DEV readiness removed. **R5-F01**: a forecast pending on the effective withdrawal draw remains historical evidence but is **never scored** when results later arrive.
- **Choice F (entry 127):** An infrastructure readiness marker and `deploy/INFRA_MANIFEST.ini`; strict add-only versioned helpers. Wrong helper means new helper plus unmarked successor variants for owner review; `Make_Successors` never silently withdraws or overwrites old variants.
- **R5-F02:** Deterministic, non-self-hashing readiness marker scope; no editor/cache files, no separate receipt framework.
- **R5-F03:** Short, successful-path synthetic N-1 smoke for every newly installed variant/game in **target's own Python** using target-local scratch only, not canonical research records. Do not mistake an insufficient-history response for a successful forecast.
- **R5-F05:** No automatic full-history PROD recomputation on every infrastructure reinstall. Use proportionate tests and deeper scrutiny when scientific semantics (N-1, ranking/readout, scoring, OV-1) may be affected. Do not call a tiny sample universal proof; no QA prerequisite for PROD.
- Keep strict target-visible N-1 isolation, each variant's immutable scientific identity, TOP and WORST from same frozen ranking, no game pooling, complete cumulative leagues, correct separate prevailing and exploratory OV-1, no automatic performance-based culling, appropriate owner-only withdrawal, exact manual restore with no automatic later releases, and process/orphan no-kill safeguards.

## 8. Disposition of Claude's six questions from `DRAFT_CONTRADICTIONS_FOR_REVIEWER_v0_1.md`

| Question | Current disposition |
|---|---|
| Q-a: Missed/misread contradictions? | Reviewer checked S1–S12 and D1–D8 against the referenced lines; no material misattribution identified. **Add new requirements in this handback**, notably the QA software reset and backup-gate override. |
| Q-b: Where incompatible copied lists live? | **Warn, ignore, continue** fixed; simplest safe path/fingerprint collision mechanism **still for Claude to design**. No automatic complex import/archive service. |
| Q-c: Reset and OV-1? | Reconstruct **ALL** dependent outputs correctly. QA/DEV recalculations are sandbox, never masquerading as original prospective evidence. |
| Q-d: QA/DEV `FORWARD_FROM`? | No separate formal prospective-source ritual in QA/DEV. Preserve PROD-specific eligibility and provenance, with the minimum correct QA/DEV treatment. |
| Q-e: Optional export path/passive mode? | Complete manually triggered DEV/QA reseeding is a **required software capability**; discard passive-export mode. |
| Q-f: Extra GitHub source ZIP? | No. Owner's full local E: project-folder ZIP replaces it (entry 131). |

**New engineering gap not previously covered by S1–S12/D1–D8:** owner-selectable **PROD SOFTWARE -> QA wipe-and-replace reset**, keeping QA's own role/configuration/environment and without automatically copying research data. This is distinct from PROD RESEARCH DATA -> QA/DEV reseed. Include both explicitly in EX_266.

## 9. Minimal worked scenarios and tests requested for design review

These are reviewer-proposed **design acceptance cases**, not preapproved algorithms:

**A. QA software reset:** PROD has V1/V2 with infrastructure I1. QA has V1 plus experimental V3 and infrastructure I2. Owner chooses the software reset from PROD. QA's **installed software** becomes V1/V2 + I1; V3 and I2 are gone from active QA software. QA's **own INI, `.venv`, role, backup root and locally valid control state** remain/re-establish; no copied PROD runtime control records. QA's research data is **not** implicitly copied. Verify source PROD unchanged; handle any prior QA research incompatibility without silent reuse.

**B. Research-data reseed only:** QA has I2 and V3. Owner reseeds **all active research data** from PROD. QA retains its software, controls, INI, `.venv`; the complete research copy replaces prior QA data. Mismatched/absent variants warn and are ignored locally without blocking compatible work. No PROD byte changes on success, interruption or failure.

**C. Both, deliberately:** The owner invokes A and B separately, producing a PROD-equivalent QA software/data baseline with QA-specific runtime, settings, roles and controls. No claim of runtime equivalence unless tested.

**D. Reset replay J..N:** The selected QA/DEV range is replayed, and every downstream dependent score, league/report, pending forecast and OV-1 output is correctly reconstructed or truthfully truncated for later catch-up.

**E. Infrastructure overwrite:** Warning, explicit YES/NO with **NO preselected**, accurate statement of backup/environment consequences; NO causes no overwrite; YES may proceed without backup scan. Any attempted backup failure is never misrepresented as a recovery point.

**F. Withdrawn pending forecast:** Forecast for T is outstanding, withdrawal effective T, T result arrives: preserve forecast, never score, never admit into league/OV-1 as eligible.

**G. Role/source safety:** QA role/path alias to PROD refuses both copy modes; an interrupted QA software reset cannot leave a falsely READY QA; PROD remains byte-for-byte unchanged after any source read operation.

## 10. What remains for Claude, versus what the owner has decided

No broad owner-policy question remains necessary before EX_266. Claude should propose simple **design mechanisms** for: safely wiping and replacing only QA installed software from PROD; preserving/revalidating QA INI/.venv/control state; ensuring QA research compatibility after a software-only reset; incompatible copied data path handling; truthful QA/DEV OV-1 labelling/cohort calculations; an owner-scope reset/replay with fully consistent dependent results; and proportionate INFRA testing. If any proposal entails material extra administrative complexity, **show why it is necessary and give the owner a leaner alternative** before adopting it.

The two unratified drafts still need all 20 previously documented contradictions S1–S12 and D1–D8 resolved, as well as EX_264 F01–F05 and EX_265's corresponding refinements. New owner directions in this document are newer than the committed decision log and **must be recorded accurately** by Claude without converting reviewer advice into an owner decision. Maintain `CONTINUITY_NOW.md`. EX_266 still requires a separate explicit owner GO, independent ChatGPT review and owner ratification; it does not authorise coding or operations.

## 11. Source locations

- `exchange/DECISIONS/DECISION_LOG.md`, especially entries 122, 124, 126–131, 134.
- `exchange/EX_264_ChatGPT.md` — R5-F01–F05 and notes.
- `exchange/EX_265_ChatGPT.md` — the owner's earlier decisions and reset/reseed scope (§§1, 5–8).
- `exchange/CLAUDE_WEB_TOOLS/simplify/DRAFT_CONTRADICTIONS_FOR_REVIEWER_v0_1.md` — S1–S12, D1–D8, Q-a–Q-f.
- `exchange/CLAUDE_WEB_TOOLS/simplify/SYSTEM_SPECIFICATION_DRAFT_v0_3.md` — particularly §§2, 5, 7, 10, 12, 14, 17, 19.
- `exchange/CLAUDE_WEB_TOOLS/simplify/DEPLOYMENT_DESIGN_DRAFT_v0_9.md` — particularly §§1–6 and 8–12.
- `exchange/CLAUDE_TAKEOVER_NOTE_2026_11_21.md` and the installed H-1 v7r1 for roles/protocol.
- **The owner's newer remarks in this current ChatGPT conversation**, not yet recorded in Git: latest R5-F04 operator-warning choice, required manual research-data reseed, complete consistent reset/replay, descriptive prevailing-OV-1 field, QA's variable baseline, and newly required QA software reset-from-PROD operation.

**This file is deliberately NOT `EX_266` or another EX. It is for the owner to relay to Claude.**