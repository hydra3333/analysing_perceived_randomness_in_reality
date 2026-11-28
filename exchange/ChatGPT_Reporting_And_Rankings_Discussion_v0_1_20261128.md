# Reporting and rankings - three-way discussion paper v0.1

Date: 28 November 2026
Project: hydra3333/analysing_perceived_randomness_in_reality
Status: DISCUSSION ONLY. No design ratification, code, installation or run authority.
Prepared by: ChatGPT independent reviewer, incorporating the owner's latest discussion directions.
Replies to: exchange/Claude_Reporting_Part_And_Rankings_Proposal_v0_1_20261128.md
Source baseline: main 6c71997e93cfb791436e4b58f5382437188380c8, decision log entries 410-411.

## 0. Purpose and how to respond

The owner finds the existing league reporting inadequate and wants the ranking requirements put right before
the repository tidy. This is an iterative discussion paper: table the possibilities, identify agreements,
alternatives and unresolved questions, then seek consensus. The owner is comfortable with a large initial
set of rankings, with a convenient way to switch individual reports off later. Do not arbitrarily narrow
the scientific inquiry. Equally, a catalogue is not an instruction to build everything at once.

Claude is invited to respond against the sections and criterion IDs below, with agreement, alternatives,
practical costs, and recommendations. No separate finding-number scheme is necessary; the existing MR
identities and section numbers suffice. Do not turn this into a new administrative system.

The reviewer has read Claude's v0.1 proposal, R3 v0.5 section 17, specification v0.6 sections 1.2 and 9,
and the relevant living scoring, reporting, job and fingerprint code. No project software was executed.
Claude's MR1 prototype and runtime have not been independently tested. The owner's latest positions below
are provisional discussion positions, not ratification of a final design.

## 1. First resolve the TOP/WORST question

CONFIRMED: the living system already scores two tickets per method variant per applicable target.
The scientific model generates one ranking per barrel. TOP uses the highest-ranked legal set and WORST
the lowest-ranked legal set (disjoint within a barrel). Powerball TOP and WORST each additionally use
the corresponding highest/lowest Powerball label. Oz Lotto has one seven-number ticket per readout;
supplementary matches affect the scoring and prize division, not prediction of a supplementary barrel.

The scorer in a_p_r_i_r_DEV/src/research/scoring.py (SCORED_SETS, score_content) computes separate matches,
supplementary matches where applicable, and prize divisions for top and worst. This is already implemented.
It does not fit a second independent mathematical model for WORST, nor does the owner ask it to do so.
Each readout is a separate forecast stream for performance evaluation, derived from the same ranking.

Example, invented identities and ticket descriptions:

| Variant | Readout | What is scored |
|---|---|---|
| A | TOP | A's most likely seven main numbers plus its most likely Powerball |
| A | WORST | A's least likely seven main numbers plus its least likely Powerball |
| B | TOP | B's most likely seven main numbers plus its most likely Powerball |
| B | WORST | B's least likely seven main numbers plus its least likely Powerball |

All four are separate tracks, mixed together for ticket-based ranking purposes without preference.
A WORST track high on a hit-based list, or a TOP track low on it, can be an interesting inverse pattern.
A WORST track low on a list can also be interesting: its supposedly unlikely labels really were avoided.
Both tails matter; no automatic scientific finding follows. Do not change TOP/WORST construction or scoring.

The reviewer's previous illustrative table showed selected rows only; it was not intended to imply that a
variant supplies only one readout. There is no STOP required on this account. Owner/Claude/reviewer agree on
this concept, subject to Claude confirming the clarification. Forty variants currently give 80 tracks per
game, subject to availability/status, not 80 independent mathematical models or independent tests.

## 2. Architecture and positions on Claude's Q1-Q7

| Topic | Claude v0.1 | Reviewer | Owner's latest position |
|---|---|---|---|
| Q1: separation | All printing out | Agree; all now | Agrees |
| Q2: MR1 reference | Exact rather than N1 | Agree if validated; label approximations | Agrees |
| Q3: sigma display | One signed Z; separate tails in CSV | Agree; preserve exact definitions | Agrees |
| Q4: yardstick | Independent typical; Bonferroni guarantee | Conditional reference only in actual exploratory work | Agrees |
| Q5: dependence | Note; ask about near copies | Note sufficient initially | Agrees |
| Q6: staleness | Remove invalid historical reports, regenerate on request | Initially agreed; refine as below | Prefers remove AND recalculate; clarify scope |
| Q7: R3 reconciliation | Initial subset, add rest later | Explicitly table all; no silent omissions | Discussion and consensus; large set welcome |
| Reporting separation | src/reporting/, own fingerprint | Agree; check install/copy/restore boundaries | Provisional agreement |
| Output | Text and CSV | Keep; add Excel option | Interested in multi-tab Excel and charts |
| Criterion selection | Add criteria later in code | Declarative registry and editable settings | Wants convenient on/off, preferably no code edit |
| Installation | DEV-QA-PROD or DEV-PROD-copy both to QA | Either; B reasonable after proof | Owner decides at installation |

Keep forecasts, scores, and computation of both OV-1 series in the scientific engine. Move all presentation,
including the next-draw and OV-1 print-outs, now. Reporting reads validated stored records and computes
evaluation measures, never fits methods, fetches results, scores predictions again, or changes scientific
records. No report is an input to a scientific method. OV-1 mathematics stays unchanged and main-only.

The separate reporting launcher should use the same tree settings and lock, not the engine's mutating
preparation path. Report-only operation must not trigger a scientific rebuild. Include reporting files in
infrastructure installation, flags, software enumeration, creation/copy/restore and verification, while
excluding them from the scientific fingerprint. Ensure report-only helper changes do not migrate back into
the scientific fingerprint inadvertently. No new deploy utility. Widen the known install-message wording.

## 3. Ranking catalogue and comparative positions

### 3.1 How to read the table

This inventories all existing R3 v0.5 section 17 measures, not merely Claude's initial six. The table
distinguishes the measure from the sort order. For one measure, different sort keys can yield useful
distinct rankings while sharing exactly the same underlying computed numbers. Suffixes such as RATE,
RAW and Z below are proposed display/sort IDs, not new ratified scientific measure identities. Reconcile
the names with R3's existing MAIN/PB, X/C/B and division conventions. Use clear names in every heading.

Track = one TOP or WORST ticket; ranking = full method ranking; probability = native probability forecast;
pair = TOP/WORST contrast. The same 80 track rows and fields work for track-based reports. Future ranking,
probability and pair reports use their appropriate units, not duplicated TOP/WORST tests.

Claude's column refers strictly to the v0.1 proposal: 'later' means not among its initial measures, not
disagreement or rejection. The reviewer column is a discussion preference, not a demand to implement every
item in the first change. The owner welcomes a broad set, retains his 90/7/3 criterion, wants both barrels
evaluated, and is provisionally receptive to the reviewer's additional criteria. Specific phasing remains
open. 'Retain' means keep the research definition and do not lose it at the tidy or during simplification.

| Measure / proposed sort | Short name / meaning | Unit | Claude v0.1 | Reviewer position | Status for discussion |
|---|---|---|---|---|---|
| MR0 | Best prize divisions | Track | Initial, lexicographic | Agree, preserve tie rule | Agreed direction |
| MR1.RAW | Prize rarity bits/draw | Track | Value, not own sort | Separate descriptive sort | Proposed separation |
| MR1.Z | Prize rarity against luck | Track | Initial, exact Z | Agree, validate tail | Agreed subject to numerics |
| MR1-T | Owner's 90/7/3 | Track | Initial | Agree, unchanged weights | Agreed |
| MR2 | Division recurrence period | Track | Later | Retain, per division | Later / phase open |
| MR3 | Division due alignment | Track | Later | Retain, descriptive | Later / phase open |
| MR4.C.D / ANY | Any prize significance | Track | Initial MR4 | Agree; existing cumulative case | Agreed |
| MR4.X.d | Exact division wins | Track | Later | Include all divisions, shared calculation | Expand initial set |
| MR4.C.d | Division d or better | Track | Later except ANY | Include all, deduplicate identical tests | Expand initial set |
| MR4.B.2-3 | Divisions 2 or 3 | Track | Later | Include owner's original band | Expand initial set |
| MR4 raw count/rate | Observed prizes | Track | Counts shown | Optional descriptive sorts; retain counts | Discuss |
| MR5.MAIN / PB | Mean drawn-number rank | Ranking | Later | Retain; consider early | Core R3, phase open |
| MR6.MAIN / PB | Log probability quality | Probability | Later | Retain native-probability requirement | Later / capability |
| MR7.MAIN.RATE | Main hits/draw excess | Track | Shown, not separate sort | Keep existing useful sort | Proposed separation |
| MR7.MAIN.RAW | Total main hits excess | Track | Total shown | Retain R3 raw total-excess sort | Proposed separation |
| MR7.MAIN.Z | Main hits significance | Track | Initial MR7 | Agree, exact convolution | Agreed |
| MR7.PB.RATE | Powerball hits/draw excess | Track | Shown, not separate sort | Separate sort | Proposed separation |
| MR7.PB.RAW | Total Powerball excess | Track | Total shown | Retain PB analogue | Proposed separation |
| MR7.PB.Z | Powerball significance | Track | Initial MR7.PB | Agree, exact binomial | Agreed |
| MR8 | Longest match streak | Track | Later | Retain, exact run law | Later / phase open |
| MR9.MAIN / PB | Early-late change | Track | Later | Retain, directional | Later / phase open |
| MR10.MAIN / PB | Discounted top-rank gain | Ranking | Later | Retain | Later / phase open |
| MR10.BOTTOM.MAIN / PB | Discounted bottom gain | Ranking | Later | Retain inverse counterpart | Later / phase open |
| MR11.MAIN / PB | TOP-WORST contrast | Pair | Later | Retain; useful paired control | Later / phase open |
| MR12.MAIN / PB | Match surprisal | Track | Later | Retain, not same as prize rarity | Later / phase open |
| MR13.MAIN / PB | Tilt Bayes factors | Track | Later | Retain; separate plus/minus | Later / phase open |
| MR14.MAIN / PB | Probability fidelity | Probability | Later | Retain, mathematical analogy | Later / capability |
| MR15.MAIN / PB | Spectral periodicity | Track | Later | Retain; N1 reference work | Later / phase open |
| MR16 | Hit rate and interval | Track | Later | Consider initial; core R3 | Expand / phase open |
| MR17 (temporary) | Whole-ticket hit score | Track | Not proposed | New joint diagnostic below | New proposal |

Notes to avoid omissions:

- D = 9 for Powerball, 7 for Oz Lotto. MR4.C.D is any division; MR4.C.3, MR4.B.2-3 and MR4.X.3 retain
 the owner's original division 1-3, 2-3 and 3-only questions. Identical event definitions count once.
- MR2/MR3 are per division. MR8's R3 default is main matches >= 3, not an arbitrary tuned threshold.
- MR16 submeasures: ANYDIV, every PDd/ODd, M2/M3/M4, PB (Powerball only). Preserve observed rate,
 exact interval (constant-rate reference), expected count, local 3-sigma observed-rate threshold and
 power at 1.5x/2x. Do not count the same binomial hypothesis twice with MR4.
- R3 requires descriptive and significance sorts where relevant. Retain raw quantities and significance
 as different sorts; exact rank keys, secondary keys and tied-rank display to be agreed. MR7's ratified
 descriptive total excess and the current useful per-draw excess are distinct when n differs. MR0 uses
 lexicographic division count vectors, with MR1 tie-break on own-set histories per R3. MR1-T remains
 exactly (0.90 W1 + 0.07 W2 + 0.03 W3)/n, not a newly invented significance measure.
- Preserve R3's other definitions, channels, edge cases, intervals, calibration and capability requirements.
 Do not manufacture probabilities from untyped scores for MR6/MR14. For later measures apply R3's stated
 descriptive/significance/mirror sorts rather than assuming one rank per MR family.
- Owner is unfussed by a large set that can be reduced later; discuss reasonable first delivery and runtime.
 MR4 variants reuse one simple binomial mechanism. MR5/MR16 were originally core-stage requirements.
 Suggest a first delivery including all cheap useful track measures above plus MR16 if proportionate; ask
 Claude to propose phasing, rather than infer that the owner has approved a complete implementation now.
- In-sample remains a separate, explicitly labelled hindsight diagnostic, not competitive with WF. It needs
 distinct computation and is not authorised by a reporting-only change. Preserve as deferred work, not
 silently discarded. Same for N1 uses not replaced by exact single-track mathematics.

### 3.2 MR17 (temporary) - whole-ticket hit score

Reason: a prize-based ranking measures both barrels through the prize rules, but misses combined hits that
do not win a prize. Add an explicit diagnostic using every hit. The simple initial Powerball variant:

    H_t = M_t + B_t                  # main match count plus Powerball hit (0 or 1)
    E0(H_t) = 7*7/35 + 1/20 = 1.45
    Var0(H_t) = Var0(M_t) + 0.05*0.95

The exact one-draw polynomial is A_PB(z)*(0.95 + 0.05*z), where A_PB is the main hypergeometric probability
polynomial. Its n-th power gives the total H null distribution on a fixed n grid. Show n, each component,
total, hits/draw, expected, excess, both inclusive tails and signed Z. Offer raw rate and significance sorts.
This gives every matched label equal weight, NOT equal influence to each barrel. It is a declared mathematical
diagnostic, not a prize or expected-money measure. If desired, discuss a distinct equal-barrel-scale variant
(e.g. M/7 + B) or standardized component weighting, clearly named and separately counted; do not tune a weight
on observed performance and then imply calibration. No choice yet beyond the simple suggestion.

Oz Lotto is one barrel. MR7 already measures all winning-number hits. MR17 as above is not applicable there;
an optional different diagnostic M+S including supplementary matches can be discussed, using the joint
hypergeometric law, not treating the supplementaries as an independently predicted barrel. Do not create
a duplicate Oz MR7 hypothesis or pool games. MR17 is a provisional reporting ID, not a new E-method.

## 4. Z, exact references, and yardsticks (Q2-Q5)

For n > 0 use inclusive P_up=P(X>=observed), P_lo=P(X<=observed), Z_plus=max(0, normal_isf(P_up)),
Z_minus=max(0, normal_isf(P_lo)); signed Z=Z_plus-Z_minus. Both cannot be positive for inclusive tails.
Neutral means neither tail is below 0.5, not necessarily precisely the mean. Keep both tails and separate
sigmas in machine-readable outputs. The existing ratified excess-sigma sort (with its stated tie keys)
and a signed-Z sort are not identical; name them accurately and agree which reports are default. Never
rank by rounded displayed Z. Undefined/no observations are explicitly marked, never treated as zero.

Use exact discrete distribution calculations where feasible. MR7 convolution and MR4 binomial are natural.
MR1 is a sum of division surprisal weights b_d=-log2(p_d), including no-win weight zero. Its full discrete
tail is calculable in principle. A rounded histogram or approximate discretisation is not automatically an
exact tail: validate support ordering, equality/near-boundary cases, extreme tails and accuracy against a
small independent enumeration or an appropriate oracle; label approximation/error if used. Benchmark
before promising seconds. Replace MR1's N1 approximation only where mathematically justified. Keep N1
for other research uses, not as an admission gate. Avoid 1-p cancellation; preserve very small tails.

For a report's worked example, use its actual exact-tail computation, not the ordinary (x-mean)/sd shortcut
presented as if identical. The latter may be shown as intuition, explicitly approximate. MR0's lexicographic
order is not ranked by sigma; a best-division tail is an ancillary reference, not the calibrated probability
of that full lexicographic profile. MR1-T is a preference score; explain it as such, no invented sigma.

Every applicable report should state:

- Independent continuous reference: for 80 ideal independent one-sided tests the median maximum is about
 +2.38 sigma. An illustrative typical maximum, not an estimate of actual correlated track behaviour;
 discrete probabilities may be conservative. Both ends are interesting.
- Conditional Bonferroni reference: alpha=.05 over 80 one-sided tests gives about +3.23 sigma; over both
 ends (160 tests) about +3.42. This needs valid marginal p-values and a predeclared family; independence
 is not needed. In actual exploratory historical reports these are reference thresholds, NOT guaranteed
 error bounds. Dynamic test count for every stated scope, distinct tests once; do not hard-code 4.0.
- State precisely whether the yardstick is per list, both ends, or across named applicable criteria and
 games (no pooling of game observations). No scope includes future repeated looks unless separately
 justified. Do not claim programme-wide calibration, evidence or discovery. For non-p-value ranking
 criteria show relevant chance expectations and/or clearly labelled auxiliary references instead.

The conditional fairness and nonanticipation assumptions matter. Fixed opportunity grids are required;
data-dependent withholding/stopping can invalidate fixed-n tails. R3 17.3.7A is scientifically important.
Mark such selection unverified, retain affected counts, and show values, not suppress them. Historical
method/window/measure selection with knowledge of outcomes means exploratory, even with mechanically
N-1 forecasts. Local establishment and before-result-on-file counts do not establish prospective validity.
No automatic discovery claims, including after more draws; a formal investigation would be a separate
project with then-future outcomes. No revival of search-log, family-registration, Mode H, holdout or formal
administrative machinery. Reconcile old R3 wording explicitly with the current simplified approach.

TOP/WORST are dependent; other methods and criteria can be highly correlated or identical. Note this, do not
remove methods or pretend cross-criterion agreement is independent evidence. A simple dependence legend
suffices; automatic near-copy detection is not necessary. High rank on only one criterion may indicate
luck OR a measure-specific pattern, not necessarily luck alone. Retain both possibilities.

## 5. Comparison windows, statuses, and rank semantics

The reviewer leans to OWN_SET (each track's own scored history through requested draw) as normal, preserving
all its performance and displaying n, first/last scored draw and missing targets/reasons. R3 17.3.7 default
was common scored intersection; retain a COMMON_SET option for comparing like periods if useful. This is an
explicit open owner choice, not silently decided. Discuss whether to offer an optional start draw/window;
current cumulative whole-era behaviour and LAST/ALL/DRAW end selection must be clearly documented.
No old holdout cap. Games separate. Current population history is retrospective, not what was published then.

Keep LOW_N (<30), no-score and other statuses, retirement boundaries, ignored/refused lists, and forecast
made-before/after-result-on-file provenance. Show denominator appropriate to each track and criterion.
Use competition ranks 1,1,3 with deterministic identity order inside a true tie; compare unrounded values
and documented secondary keys. Report N applicable ranked units and total units separately. Labels and
legends should explain both readouts, actual numbers and expected counts, not require the manual.

## 6. Configurable criteria and report formats (new owner discussion)

A large inclusive registry and a small editable report-only settings JSON appear preferable to hard-coded
OK/OFF switches. Example (illustrative names, not a schema decision):

    {
      "criteria": {"MR0": true, "MR1.RAW": true, "MR1.Z": true,
                   "MR1-T": true, "MR7.MAIN.Z": true, "MR17": true},
      "formats": {"text": true, "csv": true, "xlsx": true}
    }

Ask Claude to recommend a minimal registry/config design: stable IDs, one definition and legend per
criterion, reusable calculations and sort functions. An enabled sort produces a named file; disabling a
criterion does not remove it from the research catalogue or scientific data. Clarify whether disabled
criteria still have displayed fields/rank columns, or all its fields are omitted; suggestion: separate
enabling a sort from selecting computed/displayed criteria only if needed, avoid unnecessary settings.
Refuse unknown/invalid values clearly; do not silently ignore misspellings. Use current ASCII/CRLF file
standard. Config is report-only; changing it invalidates affected reports, never forecasts or scores.
Discuss tracked DEV default distributed with reporting code versus optional local owner settings, and
copy/backup semantics. No general-purpose plugin framework, no generator or extra deployment utility.

Plain-text and CSV remain supported. Every text report has a short plain-English introduction and complete
column/criterion/status/mode legends underneath, examples from actual rows where practical, division odds,
descriptive/exploratory caveats. Same data and rank columns across sorts of the same unit/population/window.
The CSV stays rectangular for import; put explanatory text in a companion text file or workbook legend,
not variable-length prose rows inside the sortable data. Full identifiers, descriptive method names and
unambiguous numeric columns; preserve raw and log tails as needed for very small numbers. Do not lose
precision by display rounding. Workbook adds convenience, never becomes input to scientific processing.

### 6.1 Excel workbook - preferred additional format for discussion

Owner wants to open in Excel and sort/re-sort the same data to see different slices; a multitab workbook
is possible. Prefer modern .xlsx, not legacy .xls; CSV cannot have multiple tabs. Suggest one workbook per
game and requested report end draw, with named sheets:

| Sheet | Purpose |
|---|---|
| Rankings | One row per readout track, all numeric measures, rank columns, readable headings, filters and sortable Excel Table |
| Legends | Column-by-column meanings, criterion IDs/names/formulas, worked examples, status and sorting rules |
| Fair reference | Game rules/odds, expected counts, tail/sigma meanings, yardstick scope and caveats |
| Highlights | Reproducibly selected interesting observations, both directions, actual values and qualifications |
| Charts | Clearly labelled graphs with units, n/window, legend and reference lines where relevant |
| Draw detail (optional) | Long-form scored target/track/readout data for period, barrel, division and trend analysis |

Later analysis units may need separate sheets/tables, not fake TOP/WORST duplication. Use numeric cells for
numbers, blank/tagged undefined values, freeze headings and identity columns, sensible column widths,
sorting/filtering. Preserve raw tails in machine-readable form when Excel numeric precision is inadequate.
Avoid formulas that change scientific values on opening; computed numeric values authoritative for report.
Discuss one workbook for LAST by default; ALL potentially generates hundreds of workbooks, so owner should
be able to choose formats and scope. Prefer native XLSX writer, not Excel COM/installed Excel dependency.
Claude to check existing dependencies and recommend the simplest maintained writer, installation impact,
reproducibility tests, Excel file locks and safe replacement. No package installation now.

### 6.2 Pivot tables

Ordinary sorting/filtering of a wide rankings table may meet the immediate goal more simply than pivots.
Pivot tables are useful for grouping long-form data by family/variant, TOP/WORST, draw period, criterion,
main/PB, or prize division. A separate long-form data sheet with defined keys makes it easy for the owner
to create pivots in Excel. Do not average sigmas, ranks or p-values as if they were independent observations;
aggregate actual counts with correct denominators and avoid double-counting a track. Suggested initial
delivery: pivot-ready data and a few clear usage examples. Discuss whether prebuilt pivot tables actually
add value and whether the chosen writer supports them reliably; no requirement for complex pivot automation.

### 6.3 Automated interesting observations and charts

Owner asks whether the system can guess the top 3 or 5 interesting findings and plot them with excellent
legends, or whether this needs an AI. It does NOT need AI for a useful deterministic first version.
Call them 'research highlights' or 'observations worth inspecting', not findings/discoveries. A transparent
reproducible rule can flag, for example:

- largest positive and negative local signed Z in applicable ticket-based measures, with both ends visible;
- unusually high or low WORST performance, or TOP/WORST contrasts (MR11 when implemented);
- strongest full-ticket and prize-division performance, including rare actual top divisions;
- distinct patterns across criteria (not independence), and changes/streaks when those measures exist.

A possible top-5 selection policy: nominate candidates by declared category, choose by a stated numeric
rule within category, deduplicate substantially identical event/track highlights, show n, raw values,
reference, relevant ranks and why chosen. If fewer meaningful candidates exist say so; do not force five
or require crossing a threshold to report. Avoid claiming a global 'most interesting' order across unlike
measures; category-specific choices are more interpretable. This is a reporting aid, never a method filter.
Example charts: diverging signed-Z bars showing both extremes; observed vs expected main/PB hits or prize
counts for selected tracks; cumulative observed minus fair-expected hits versus draw number, with a clearly
labelled reference and visible n/coverage; separate TOP/WORST lines of one variant if useful. Do not draw
unsupported confidence bands or compare unlike units on one axis without explanation. Highlight selection
is retrospective and adds another look at the data, not corroboration. Charts must have titles, axes,
units, window, legend, concrete explanation and limitations, and link to underlying values in the workbook.

Claude and reviewer can jointly propose selection rules and chart designs. AI may later interpret unusual
patterns the deterministic rules did not anticipate; useful, but not required in the reporting engine.
No AI service, nondeterministic narrative generation or online dependency in the routine job.

## 7. Draw selection and staleness (Q6 - owner prefers remove and recalculate)

Clarify the competing proposals: currently section 9 requires a report for every scored draw and removes
obsolete reports. Claude proposes LAST ordinarily, ALL and DRAW n on request, deleting invalid earlier
reports without automatically recreating them. Reviewer initially agreed with that economy; owner now
prefers remove AND recalculate. We should respect this rather than assume deleting without replacement.

Suggested compromise for discussion: keep LAST default; whenever an existing earlier report becomes stale,
remove and regenerate the affected existing report dates in their enabled formats. A normal append creates
LAST, leaving earlier valid dates unchanged. ALL explicitly generates/recomputes every scored draw; DRAW n
recomputes the nominated valid cumulative endpoint. A change in report code/config invalidates affected
report output; a corrected earlier score/forecast or changed current population invalidates affected historical
reports; use a conservative per-game rebuild of already-existing dates if simpler than fine-grained tracking.
No need to manufacture previously unrequested dates unless the owner wants the original all-dates rule.
Ask Claude to compare this with always rebuilding every affected date, and give practical costs. Clarify
how disabling a criterion removes its outputs without re-creating disabled files, how ALL is honoured with
format options, and how a failed report rebuild leaves no old file falsely presented as current. Use the
tree lock, simple input/report version identity, safe publication and clear failure/cleanup; no elaborate
transactional framework. Forecasts and scores stand on a report failure. Explicitly amend section 9 once
agreed. No scientific rebuild for report invalidation.

## 8. Proof, specification reconciliation, and work sequence

- R3 v0.5 section 17 remains the source of the scientific measure definitions. The current exploratory
  scheme supersedes the old administrative apparatus. Amend specification v0.6 section 9 and explicitly
  document any changed R3 measure, sort, comparison-set default, mode/phase, format or calibration policy.
  Preserve every outstanding measure and its disposition; no silent loss of MRD decisions again.
- The one initial engine change triggers its ordinary rebuild; no special fingerprint bypass. Compare DEV
  before/after scientific contents of all forecasts, scores and both OV-1 series, including method identity,
  target and establishment boundaries. Exact equality for scientific content; timestamps, before-result-on-file
  and audit/computation metadata may legitimately change on rerun. State and justify any normalisations, never
  ignore scientific differences. Next-draw/OV-1 print-out relocation should match for identical scientific AND
  presentation inputs; new intentional legends and provenance differences are separate declared changes.
- Permanent proportionate invented-data tests: hand-calculated ranking measures, tails/oracles, edge cases,
  both games and both readouts, MR4 division events, exact MR17 convolution, correct N/duplicates and ties,
  opportunity-grid warnings, report-only isolation, installation and fingerprint boundaries, LAST/DRAW/ALL,
  staleness regeneration, enabled/disabled criteria, complete legends, XLSX sheets/values if agreed, deterministic
  highlights and chart data. No real updater or live-tree commands by either AI or local runner.
- No promise of exact MR1 runtime until measured. No arbitrary large implementation or extra administrative
  gates. Claude to propose a proportionate code plan, cheap first phase and any genuinely costly deferred
  measures, with owner and independent reviewer agreement before coding.
- Owner chooses deployment route A (DEV-QA-PROD) or B (DEV-PROD then Copy_From_PROD both QA) after DEV proof.
  B is reasonable for this change; it trades away a separate QA trial. No new commands needed for that route.
- Update manual, README and handovers after agreed changes, then revised tidy and P1. Keep original research
  source documents and old reporting implementation's valuable ideas through history/archive as agreed.

## 9. Requested reply from Claude

Please provide your positions, alternatives and practical recommendations on this discussion paper,
especially the catalogue (section 3), combined MR17, Excel/settings/highlights (section 6), and the owner's
preference to remove and recalculate stale reports (section 7). Identify genuine differences from R3 and
propose explicit resolutions consistent with the simplified exploratory system. The owner wants an iterative
exchange to reach consensus; no coding or final ratification is requested by this paper. Keep the discussion
proportionate and do not revive the old administrative machinery.

END.
