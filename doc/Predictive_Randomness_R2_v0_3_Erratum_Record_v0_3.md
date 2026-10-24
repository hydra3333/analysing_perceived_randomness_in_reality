# Predictive Randomness — R2 v0.3 erratum record (prior approvals plus owner-approved ERR-R2-05)

**Erratum decision record version:** 0.3 — OWNER-APPROVED 24 October 2026 (retains previously approved v0.2 §§1–4)  
**Status:** **ERR-R2-01..04 previously OWNER-APPROVED per v0.2, ERR-R2-02 still PROVISIONAL; new ERR-R2-05 OWNER-APPROVED 24 October 2026.** R2 v0.3 remains ratified.  
**Target:** `doc/Predictive_Randomness_Experimental_Method_Specifications_R2_v0_3.md` (ratified)  
**Context:** Claude cross-document review of Architecture v0.2 and R3 v0.1; owner's subsequent Architecture 2 / Option F / six-worker / self-contained `.bat` maintenance directions.

## 1. Purpose and authority

The **scientific** R2 contract remains intact: strict historical N−1 visibility; real FINAL forecast L+1 from all permitted data 1144..L; immutable TOP/WORST and full rankings; separate post-draw evaluation; independent real/synthetic namespaces; canonical prediction-content equality under different worker scheduling; permanent E_1–E_62 retention; B1/B10 timing-only comparisons; performance not a method veto. Nothing in this erratum changes those rules.

R2 v0.3 permits **1–12 workers**: six is already within that upper bound. The issue is the specific **1-versus-12 testing/benchmark language**, illustrative process-pool implementation choice, and package-record wording. The owner has since specified **configurable 1–6 workers, default and initial maximum six**; standalone `.py` E-methods coordinated provisionally through `Run_Experiment.bat` using `subprocess.Popen`; and the project's human-maintained dependency authority within `install_upgrade_dependencies_into_venv.bat`.

**Authority and preservation:** On 22 October 2026 the project owner approved ERR-R2-01 and ERR-R2-03, approved ERR-R2-04 on the author's affirmative recommendation, and approved ERR-R2-02 provisionally on the author's affirmative recommendation, subject to Windows tests and review of findings. This approved erratum accompanies the ratified R2 v0.3; it does **not** replace or modify the historical R2 file. Where the narrowly defined operational details in this erratum differ, the owner-approved provisions here govern. All other R2 requirements retain their authority. No untested launch mechanism is deemed accepted for production.

## 2. Approved narrow operational interpretation of R2 acceptance language

| R2 location | Existing concept in ratified v0.3 | Proposed narrowly changed meaning |
|---|---|---|
| I-11 | One worker per method; configurable 1–12, optional 24 SMT trial | **Retain scientific meaning** as an upper-bound capability statement. New initial project operating cap is **six**; no 12/24 baseline is required initially. A future increase needs a controlled owner decision. |
| I-12 | Same-input determinism: 1 worker versus 12 | Replace literal test pair with **one worker versus the configured maximum concurrent workers (currently six)**. Retain bit-identical canonical forecast content by default and user-approved exception discipline. |
| §9.1 / R2-D07 | `ProcessPoolExecutor` or equivalent spawn-safe process worker pool / 1–12 pool | Clarify that separately executable E-method `.py` files under a `subprocess.Popen` coordinator (provisionally through the common protected batch wrapper, Option F) are an **acceptable implementation** of process isolation/one method per worker. Initial concurrency **1–6**. This does not authorise different mathematical fit behaviour. |
| §10.2 step 2 | `workers=12` | `workers=<configured maximum>` (initially 6), matched to the serial test jobs. |
| §10.2 step 7 | Optional 24 workers after 12 | **Defer** 12/24 scalability trials unless the owner explicitly elects to explore a higher limit. Do not treat such a trial as initial acceptance. |
| §11.1 T-13 | One versus twelve workers | One versus configured maximum workers (currently six), identical canonical forecast bytes. |
| §11.1 T-37 | Serial versus twelve stochastic TOP/WORST run | Serial versus configured maximum (currently six), including complete rankings, TOP/WORST and availability status. |
| §11.3 | Repeat-test one and twelve workers | Repeat-test **one and configured maximum** (currently six), same env/seeds and canonical-content boundary. |
| Stage S3 | 1/12-worker execution | **1/configured-maximum-worker** execution (initially 1/6), plus B1/B10 unchanged. |
| R2-D09 | Canonical bit identity 1 vs 12 | **Canonical bit identity 1 vs configured maximum**, default 6. |
| §12.4 example CLI | Example `--workers 12` | If retained as a current illustration, use `--workers 6` and describe it as a nonbinding example; real approved CLI may instead use batch wrappers. |
| §12.3 dependency version record | Versions recorded in `requirements.txt` **or an explicitly named supplementary lock specification** | Name **`install_upgrade_dependencies_into_venv.bat`** as the sole human-maintained authoritative dependency list and install/upgrade procedure. Generate and commit a machine-readable **resolved Python/PyPI version snapshot** with consequential benchmarks and each genuine FINAL batch; no second independently maintained package list. |

### 2.1 What stays unchanged

- Historical leakage and immutability checks, including T-05, remain mandatory.
- A method's fit seed cannot depend on the entire source snapshot, worker count, execution order, or TOP/WORST readout formatting.
- `selection_model_version` in R2 §9.2 retains the meaning of the actual stochastic **fit sampling/observation model**, not downstream TOP/WORST readout. Any prediction-time tie-breaking seed/key belongs to its own independently versioned readout domain, per proposed R3 v0.2.
- Scores, synthetic firewall, holdout boundaries, all-method retention and user control of ratification remain in force.
- Benchmarks continue to report resource and time data, not predictive merit.

## 3. Acceptance requirements and outstanding test gates

1. **Identity:** Given the same canonical training view, method revision, fit configuration, target and environment, compare complete prediction-content bytes under one worker and six simultaneous workers. Changes in worker ordering must not change the forecast; timestamps/resource measurements are not part of canonical prediction content.
2. **Launcher equivalence:** Manual `Run_Experiment.bat` and coordinator-launched `Run_Experiment.bat` execute with the same validated `.venv`, arguments and numerical thread controls and produce identical canonical method outputs.
3. **Dependency provenance:** A consequential benchmark or FINAL forecast records the actual Python version, resolved installed PyPI versions, self-contained maintenance-script revision/digest and applicable Git identity. A pip-upgrade is a separate explicit operation, never implicit on a prediction launch.
4. **Windows gate:** CMD argument quoting, batch exit codes, Ctrl+C and `psutil` process-tree termination must pass P0/P2 testing on Windows. No Python-redirector-specific PID assumption is permitted.
5. **Future extension:** Reopening a higher worker count or experiment-created subprocesses must have an explicit owner-approved change and tests, not a hidden escalation.

## 4. Project-owner decisions — 22 October 2026

| ID | Decision | Owner disposition | Implementation consequence |
|---|---|---|---|
| **ERR-R2-01** | One-versus-configured-maximum worker equivalence, initially **one versus six**, replaces literal one-versus-twelve testing | **APPROVED** | Tests and benchmark instructions use configurable 1–6 worker capacity, with canonical prediction-content identity preserved. No compulsory 12/24-worker trial. |
| **ERR-R2-02** | Standalone E-method subprocesses, provisionally launched by the coordinator through protected `Run_Experiment.bat` (**Option F**) | **APPROVED PROVISIONALLY**, on the author's affirmative recommendation; **subject to Windows testing and review arising from the findings** | Option F is the first implementation to prototype, **not** a passed production design. Run P0/P2/W-suite tests covering argument fidelity, exit codes, streams, Ctrl+C, process-tree termination, Python/venv behaviour, direct/coordinated identity, and six-worker concurrent execution. If substantive failures arise, document and review them before deciding whether to correct Option F or select direct launch. |
| **ERR-R2-03** | `install_upgrade_dependencies_into_venv.bat` is the **sole human-maintained dependency authority**, accompanied by generated resolved-environment snapshots | **APPROVED** | Maintain the package list and install/upgrade logic in the batch file; no second independently maintained requirements list. Archive actual Python/PyPI versions and maintenance-script revision/digest with consequential benchmarks and every FINAL batch. Upgrades are explicit maintenance actions only. |
| **ERR-R2-04** | Clarify the meaning of `selection_model_version` and keep stochastic **fit** seeding independent of TOP/WORST **readout** selection/tie rules | **APPROVED**, on the author's affirmative recommendation | `selection_model_version` in ratified R2 §9.2 denotes a version of the mathematical sampling/observation model that actually influences fitting. Readout/tie-breaking gets its **separate versioned and seeded domain** as proposed for R3. A changed reporting or tie-readout rule cannot change fitted stochastic state. No retroactive rewriting of R2 v0.3. |

### 4.1 Rationale for the conditional and recommended approvals

- **ERR-R2-02:** Recommended because using the same protected wrapper for manual and coordinator-launched experiments reduces duplicated launch behaviour while retaining independent executables, live output, argument passing and subprocess isolation. The cost is an extra CMD process and Windows-specific argument/interrupt/termination details; these must be proved on the actual machine before implementation acceptance. No project-managed Windows Job Objects are introduced as part of this decision.
- **ERR-R2-04:** Recommended because stochastic fitting and deterministic readout are mathematically distinct. Conflating their version identifiers could alter the fitted state merely because TOP/WORST presentation or tie-breaking changes; that would defeat the project's reproducibility and clean interpretation requirements.

### 4.2 Outstanding work — not implied to be approved or complete

1. Verify Option F under Windows P0/P2/W-suite tests. **No tests have yet been run under this erratum.**
2. Review any failures and approve remedies before certifying the launcher for consequential experiments or FINAL forecast batches.
3. Resolve R3's tie-break versioning/implementation in its own review and ratification cycle.
4. Retain `Predictive_Randomness_Experimental_Method_Specifications_R2_v0_3.md` intact; keep this erratum alongside it as the dated decision record.

**End of preserved v0.2 approved erratum text. Owner-approved ERR-R2-05 follows.**

## 5. ERR-R2-05 — owner-approved per-game R2 scientific and execution contracts (24 October 2026)

**Approved:** 24 October 2026. **Authority:** owner-approved narrow per-game interpretation under ratified charter Proposal v0.4. Earlier ERR-R2-01, 03 and 04 remain approved, and **ERR-R2-02 remains provisionally approved** pending P2; nothing here changes those statuses. The historical text in §§1–4 above records earlier approvals and is preserved verbatim. This approved narrow section takes precedence over R2 v0.3's Powerball-only examples **only where game scope is involved**; all unchanged R2 conditions continue to apply separately to both games.

| R2 contract area | Proposed additional requirement | Required review evidence |
|---|---|---|
| I-05 / I-06; eligible real observations | Bind each run to an approved `game_id`, frozen era/profile version and permitted source snapshot. The target belongs to the profile's era; no mixed-era observations. `POWERBALL` remains 1144 onward, Oz Lotto 1474 onward, seven winning labels from 1..47. Oz supplementaries are excluded from all scientific views, preserved only in a separate raw file. | Era/range/supplementary negative tests and same-game N−1 suffix-poison tests. |
| Dataset and holdout | Per-game isolated source, development, FINAL, holdout and synthetic namespaces. Powerball 1578–1587 remains sealed. Define Oz holdout by the **ten highest draw numbers in its first structurally accepted winning snapshot**, fixed before the first scrape; save exact range and snapshot hash afterward. **Historical development/backtesting targets only remain below the first sealed holdout draw:** Powerball `N ≤ 1577`; Oz `N ≤ holdout_first − 1`. A target after the holdout cannot be treated as development, since its permitted N−1 history would include sealed observations. Post-holdout targets enter only the separate prospective FINAL track or a separately owner-approved and reviewed protocol. A bounded structural audit may validate held-out rows but never reveal values. | Pre-scrape rule, seal record, audit output-schema test, poisoned holdout-value test showing no model exposure. |
| Target identity | The unique draw identity is `(game_id, draw_number)`; draw number alone is insufficient. New canonical wrappers/status/manifests require both fields; `draw_key` is display only. Prior v0.1 Powerball records are read using an explicitly versioned compatibility rule, never silently rewritten. | Duplicate draw numbers across games; mismatched-game scorer refuses. |
| Permitted U / ordered / X views | Game-specific canonical view schemas with independently versioned identities. Existing Powerball `E1_REAL_U_TRAINING_VIEW_V1` and its approved digests remain **byte-identical**. Oz U contains seven winning labels only and no fictitious PB channel. Method declarations specify barrel and view needs; missing/unsupported is explicit, not silently substituted. | Powerball synthetic and real-1577 golden regression, synthetic one-barrel 7-of-47 fixtures. |
| Seeds and tie identity | The R2 permitted-view SHA-256 remains the input identity for fit seeds and R3 `TIE_SHA256_V1` readout. **Every NEW permitted-view schema for ANY game**, including new Powerball E_2+ U/ordered/X/date-derived views, binds `game_id`, era and profile version through its schema/domain and digest. **Only** the pre-existing Powerball `E1_REAL_U_TRAINING_VIEW_V1` retains its legacy domain byte-for-byte. No full CSV hash, future row or post-draw score enters the content identity. | Target/future-row mutation, independent tie-key vectors, deterministic 1-vs-configured-maximum tests. |
| R2-C13 method registry | Every E-number has a status per game: `SUPPORTED`, `FORMULA_OPEN`, or `UNSUPPORTED_FOR_GAME` with a structural reason and versioned method identity. Lack of a second barrel does not cause invention of one. Method hypotheses remain permanently registered, not vetoed because theory predicts chance performance. | Completeness test for every method × game, per-barrel support assertions. |
| Date-using views | Each profile fixes `(first_draw, first_date)` and hence the derived weekly date. Verify source dates for all snapshot rows via bounded audit, not as U inputs. E_14/E_54 views bind their derived-date mapping through profile/version + schema and included draw identities; discrepancies block date-dependent methods for that game until owner resolution. E_54's external-covariate availability gate remains separately FORMULA_OPEN. | Simulated date anomaly: date-dependent refusal without ball-value leakage; original Powerball U digest unchanged. |
| Historical/FINAL boundaries | Training uses draws less than N in the selected game, target row N never parsed by a method; **historical development/backtesting requires N < holdout_first**. This is not a global operational or maintenance cap: separately authorised prospective FINAL forecasting, eligible weekly retraining and post-draw scoring can progress beyond that boundary, subject to N−1, freeze, source eligibility and holdout policies. The holdout is not opened by this approval. FINAL uses only known draws up to L and predicts L+1, with game-specific publication deadlines and its separate holdout policy. Scorer separately reads exactly the authorised game+target outcome **after** verifying the frozen forecast. | Cross-game same-number collision, suffix poison and separate outcome-stage tests. |
| Failure and result firewall | A result from a FAILED or orphan-suspected group **must never be consumed**, even if `canonical_result.json` exists. Global orphan marker governs launches for every game. Full process identity/creation time/status ownership and standalone exceptions remain as ratified. | Forged PASS, wrong game/target, orphan-marker and late-result rejection tests. |

**Owner-ratified clarification (24 October 2026):** The holdout-based ceiling restricts historical development and retrospective evaluation ONLY. It does not impose a permanent upper limit on future prospective FINAL predictions, normal operations, maintenance, or retraining on subsequently eligible known draws. Holdout observations remain sealed for development, and any prospective use is governed by separately authorised FINAL and holdout rules.

**Decisions intentionally left OPEN:** exact Oz Lotto snapshot identity until an accepted first scrape; nominal local draw/closing times and UTC conversion (including DST) until operator verification; E_54 known-before-draw external-feed contracts; each method's `FORMULA_OPEN` settings; first Oz Lotto real experiment; start of each game's FINAL track; cross-game scientific features. The current pre-development window for Powerball 1145–1577 is separately under evaluation-window review, not implicitly ratified here.

**No authorisation:** This owner-approved ERR-R2-05 does not permit reading held-out outcome values, Oz Lotto method execution, destructive tests, changing `ENABLE_PROCESS_TERMINATION`, removing an orphan marker, or modifying a frozen Powerball result.

