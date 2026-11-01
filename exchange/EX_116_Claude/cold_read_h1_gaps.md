# Cold-read test of H-1 v1r7 (candidate 1): the 20 gaps found, and how candidate 2 resolves each

Date: 1 November 2026. Written by Claude from the report of a fresh helper agent that was given only the
repository and the new H-1 (candidate 1 of the DOC-10 snapshot) and asked to explain the project back and to list
everything it could not find or found contradictory. The helper opened nothing under source_data/, results/ or
transitory_data/, ran no program and changed no file. It also did not open R1, because of the paragraphs that
name quarantined draws (gap 12).

What the helper got right without help: the project, the roles, the hard rules, the state (installs, batches,
both reports, 471 tests), the next three pieces of work and the goal date, the package mechanics, and where the
tools are.

| # | Gap found (file and section) | Resolution in candidate 2 |
|---|---|---|
| 1 | H-1 section 3 says weekly forecasting starts only after modelling is complete, while GOAL-1 asks for forecasts from 9 November and "declare developed" before waves 3-11; "prospective mode", "FINAL" and "production weekly loop" are never mapped; the roadmap's "Later" list is stale | H-1 sections 3, 10 and 12.8 and register v0.23 define the prospective mode (MH-1's weekly loop) and "developed" (the pipeline declared ready for the released cohort; waves continue); FINAL's relation is recorded as OPEN for the Mode H design; the roadmap glossary and "Later" list are rewritten |
| 2 | R3 10.1(6), 10.2 and R3-D20 require a GitHub push as timing proof; OFF-1 makes it optional; not said whether an R3 amendment must come first | H-1 section 10 and register v0.23: a ratified R3 amendment, or a ratified design superseding those clauses, must precede the first prospective forecast (OPEN item for the design) |
| 3 | Mode H not stated precisely; whether Mode H's ten steps are the first catch-up steps; post-holdout draws; HX-1 flags only 1585-1586 although 1585-1588 were seen | H-1 section 10 and register: every released variant forecasts each holdout draw walk-forward, frozen before opening, scored once; the catch-up overlap is OPEN; new owner decision HX-2 (holdout never extended; 1587 and 1588 flagged when caught up), also in the holdout record v0.3 |
| 4 | H-1 10.3 cites "probe A6" for the shared-SHA point, which belongs to A1 | Corrected to A1 |
| 5 | Roadmap item 10c says the update runs "by the update process already designed" and is designed "alongside the snapshot"; header date, item 10 "NOW", glossary "Released", E_17 seeding note and "Later" list stale | Roadmap rewritten (Claude's working list, committed directly) |
| 6 | Who lifts "the owner will not run results_master update"; who writes HOLDOUT_OPENED | H-1 section 5.1 and register: the owner's separate approval at the Mode H stage for the first update run and for opening the holdout; the writer of the record is designed in Mode H |
| 7 | H-1 7.2 module map says ENABLE_CONTRACT_REAL_DEVELOPMENT = False | Corrected: True since WF-1A (WF1-3) |
| 8 | H-1 12.3 says to install requirements.txt (historical) for the 3.15 test venv | Corrected to DIRECT_PACKAGES in install_upgrade_dependencies_into_venv.bat; the owner's exact versions (report environment lines) noted; a full freeze list is not recorded (open item for R3-T50) |
| 9 | How a new chat reproduces 471 tests when the base tree deletes source_data while accepted tests read the development masters | H-1 12.3 and 12.9: build in a data-free tree; run the suite and rehearsals in full disposable clones of the frozen mirror, where accepted tests read what they are written to read (rule 2.5); Claude never opens those folders |
| 10 | H-1 1.6 says document-only installs have no verifier, but DOC-10 has one | H-1 1.6 explains why DOC-10 has a verifier |
| 11 | exchange/README.md v0.4 conflicts with H-1 (commit rights, zip inside zip, reviewer zips) | exchange/README.md v0.5 (Claude's file, committed directly); H-1 1.6 and Appendix A point to v0.5 |
| 12 | No locator for the R1 paragraphs that name quarantined draws | H-1 section 5.1 gives the line numbers and section headings only (found with grep printing line numbers only); the new chat skips them |
| 13 | How a new web session gets push access, and what to do without it | H-1 12.1 "Repository access" |
| 14 | H-2 v1r8 section 3 still says R-8..R-11 are "proposed"; H-1 treats them as rights | H-1 1.4: ratified (register; H2-TAKEOVER-O01); H-2's wording stays only because its rights region is byte-identical |
| 15 | "No manual Lott check in production" has no source | H-1 12.8 cites the reviewer handover v10, line 250 |
| 16 | Appendix A and section 4 stale or incomplete; section 0's check of "the edition the register names" cannot work | Appendix A lists register v0.23, H-2 v1r8 and blurb, holdout record v0.3, Architecture v0.9, rulebook v0.3 and exchange/README.md v0.5 with hashes; this file is identified by the DOC-10 manifest; section 4 lists every template file's hash; section 0 step 1 checks against the manifest |
| 17 | R-009 and R-011 still OPEN though done in the snapshot; R-006's "4%" claim; the probe findings file not pointed to | Reminders (committed directly): R-009 and R-011 "in DOC-10 (pending install)", R-006 reworded per EX_099 C01, R-012 points to exchange/EX_116_Claude/cold_read_probe_findings.md; H-1 12.8 points there too |
| 18 | H-1 8.6 does not tell the new chat to check for the owner's settings.json deny entry before writing a task file | Added to H-1 8.6 |
| 19 | --bare in H-1 12.3 versus --mirror in the tools README; snapshot tools hard-code /home/claude/work/snap/ | --mirror throughout; the hard-coded path noted in H-1 12.2 |
| 20 | No schedule, draw days or fallback for the 9 November goal | H-1 section 10 "Schedule": Oz Lotto Tuesday 10, Powerball Thursday 12 November; the critical path; new owner decision FB-1 (slip a week rather than rush) |

The two owner decisions this test prompted (HX-2 and FB-1, 1 November 2026) are recorded in register v0.23.
