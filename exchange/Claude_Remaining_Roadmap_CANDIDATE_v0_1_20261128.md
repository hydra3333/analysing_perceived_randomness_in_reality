# The remaining roadmap (living document)

Project: hydra3333/analysing_perceived_randomness_in_reality.
**The owner's roadmap of 28 November 2026, endorsed in full by the reviewer and by Claude** (decision log entry
426), with the reviewer's three qualifications worked in. It is the agreed order of the remaining work. It is not
a new administrative framework and adds no approval step: each stage still needs whatever go the work itself needs.
**Kept by:** the Claude web chat, which updates the Status column as milestones are completed. Both handovers refer
to it from their next refresh.

| Stage | What | Status |
|---|---|---|
| 0 | Reporting design and specification | COMPLETE: RAT-74 (`b50d220`) |
| 1 | Develop, test and install reporting | NEXT: the code plan is with the reviewer |
| 1.5 | OWNER REVIEW OF REPORTING | |
| 2 | BACKUPS | |
| 3 | TIDY | |
| 4 | BACKUPS | |
| 5 | METHODS TEMPLATE / BOILERPLATE | |
| 6 | Future scientific methods: priorities and working arrangements | |
| 7 | Actual scientific research | |
| 8 | Performance engineering | Deferred |

## 0. Reporting design and specification

COMPLETE: RAT-74. The consolidated v0.5 design and specification amendment is ratified and installed in `doc/`
(`doc/Predictive_Randomness_Reporting_Design_And_Specification_Amendment_A1_v0_5.md`).

## 1. Develop, test and install reporting

- Claude's code plan, independent review and approval.
- Phase 1 implementation, numerical tests and scientific equivalence proof.
- Performance measurements and the ALL decision.
- Installation in DEV, QA and PROD.
- Phases 2 and 3 immediately following phase 1, subject to resolving any genuine missing scientific inputs.
- Update the operations manual and the handovers.

## 1.5 OWNER REVIEW OF REPORTING

With advice:

- review the latest reports;
- review the latest .xlsx, all tabs;
- also examine selected historical reports and interesting TOP and WORST performances;
- make observations and verify them independently with Claude and ChatGPT.

## 2. BACKUPS

Complete, verified backups before the tidy. Preserve the newly established working system.

## 3. TIDY

Reconcile the existing tidy agreement with the new reporting software and documents. Remove obsolete material
while retaining useful scientific research, decisions and historical knowledge. Verify that the living system
remains unaffected.

## 4. BACKUPS

Establish a clean, verified post-tidy baseline.

## 5. METHODS TEMPLATE / BOILERPLATE

- Both AIs reread `doc/CODING_PRACTICES_v0_1.md`.
- Review and simplify the existing method template.
- Develop a small working example with independently known answers.
- Establish reusable tests, documentation and implementation practices.

Keep it simple; no elaborate framework or code generator.

## 6. Future scientific methods: priorities and working arrangements

Finalise the existing draft research priorities. Include the de Broglie-Bohm inspired methods and the additional
proposals captured in the research appendices. Agree on the trial reversal of Claude's and ChatGPT's
designer/coder and reviewer roles.

## 7. Actual scientific research

Mathematical investigation, method design, implementation, independent review, testing, installation,
walk-forward evaluation and examination of the rankings. Repeat for each new method.

## 8. Performance engineering

Deferred until the project is sufficiently mature and the owner authorises it. Profiling Python, NumPy, SciPy,
multiprocessing and native-library execution. Subsequently consider selective Cython, Numba or other acceleration
where justified by measurements.

## Where earlier commitments sit in this roadmap

So that nothing already agreed is lost; none of these is new.

- **Stage 1:** the reporting code first reaches DEV, where the equivalence proof and the measurements are made;
  QA and PROD follow by the owner's chosen route.
- **Stage 1.5** takes in the results review begun on 28 November (Oz Lotto's league and the OV-1 files were still
  to be walked through).
- **Stage 3** takes in the rest of the simple scheme's step 7 (the decision log and the continuity page to CRLF;
  the continuity page cut down) and the local runner's rulebook v0.9.
- **Stages 5 and 6** hold the four deferred discussions of `exchange/OWNER_REMINDERS.md` (decision log entries 289,
  292, 299 and 398) and the dummy-method proof agreed with them. The later reminder (a rebuild marks every earlier
  forecast as made after its result) is discussed before the engine is next changed after stage 1.
