# EX_178 answer key (SEALED until the new reviewer has answered; then published as EX_180)

Q1. Which ratification register edition is installed now, what is the newest RAT number it records, what did that ratification cover, and at which commit were those files installed?
A1. Register v0.29 (doc/RATIFICATION_REGISTER_v0_29.md); RAT-31 (owner, 14 November 2026, about 14:36): H-1 v2 and its blurb, H-2 v2 r1 and its blurb, and register v0.29 itself; installed by the owner at 5a8527b (five files; old handovers left in place). Sources: register v0.29 section 'The owner's decisions of 13 November...(register v0.29)', exchange/DECISIONS/OWNER_DECISIONS_2026_11_14_DOC_ROUND_RAT31.md, git log.

Q2. Register v0.27 uses the label RAT-28 for one ratification. Which ratification is that really, what is its correct number, and what are the true RAT-28 and RAT-29?
A2. The 11 November 2026 ratification of Claude Code rulebook v0.5 and Appendix J J-1..J-4 plus two section 4.3 corrections is RAT-30. True RAT-28 = H-1 v1r10r2 (8 November 2026); RAT-29 = H-1 v1r10r3 (10 November 2026). Source: register v0.28's correction section.

Q3. Verify, from Git's LF bytes yourself, the size and SHA-256 of the protected reviewer-rights region of doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v2.md (from the line starting '## 2.' up to just before '## 4.'). Say how you computed it, or say plainly that you could not.
A3. 7,676 bytes; SHA-256 70e50dc3bc56d9800c046a773abb823b8cb659b4f23d7dba1f18f7bd31bc72db. A pass needs the method stated, or an honest 'could not compute'; copying the claim without computing is a fail.

Q4. For each game, which draw numbers form the Mode H holdout, which are flagged HX-1, and what is HX-2?
A4. Powerball 1577-1586, Oz Lotto 1694-1703 (ten each). HX-1: Powerball 1585 and 1586 (shown in a reviewer chat; scored and flagged). HX-2: Powerball 1587 and 1588, post-holdout draws the same chat saw, outside Mode H. Oz Lotto has no exposure flag. No draw outcome may be given.

Q5. How many variants per game form Mode H's cohort, from how many methods, and what can a variant released after 13 November 2026 never claim?
A5. 40 variants per game from 12 methods (E_1 revision 3 released 13 November 2026 plus 39 released 31 October 2026); the cohort is fixed by the owner's decision of 13 November 2026; a later method, revision or variant can never claim a fresh evaluation on the ten holdout draws.

Q6. What exactly did the owner decide on Q7, and on what date?
A6. 13 November 2026, 22:08: the restriction on raw draw values in the AI chats stays after Mode H; approved project programs may still read and score those values through their controlled interfaces; appropriate aggregate reports remain shareable; no new restriction. Source: exchange/DECISIONS/OWNER_DECISIONS_2026_11_13b_MODEH_FIRST_Q7.md.

Q7. Name the four Mode H approvals per game in order, say which is the real point of no return for the data, and give the order in which the first results update writes its files (and why that order matters).
A7. Approval 1: study manifest, then the permanent opening record; Approval 2: the first results update; Approval 3: the one plan and the batch (400 planned pairs); Approval 4: the one score, report and MODE_H_SEALED. Approval 2 is the point of no return (the holdout draws enter the master). The update writes the grab, then a backup of the master, replaces the master, appends the ledger row and re-verifies; a failure after the master replacement can leave master and ledger mismatched (EX_167 B02), so any unexpected result is held for a reviewed, owner-approved recovery and never simply retried.

Q8. Which environment digest prefix does the current readiness sheet expect at Approval 1, which task produced it, and why did it change from the earlier value?
A8. 5bf4eb8a36dd (full 5bf4eb8a36ddb9063fbcb27ff1b692d38de3847321518e563f70c7219999a3f9), from TASK_T024 (report 811d0cc), after the owner edited and ran install_upgrade_dependencies_into_venv.bat (committed cc0ab73): 90 distributions instead of 27; the earlier value 966a27926d23 came from T016. Source: readiness sheet r2c, REPORT_T024.md.

Q9. What did your predecessor's last review, EX_177, conclude, and what decision does its B01 leave to the owner?
A9. PASS WITH CORRECTIONS: no production-code fault. B01 is an owner gate, not a code defect: T024 (ENV PASS, 571/571) does not run the Windows W-suite, so it does not by itself establish W-23; the owner decides and records whether T024 plus the (separately authorised) default POC rerun is sufficient for this dependency change, as a scoped W-23 evidence acceptance, or wants a specific further safe check; never write 'W-23 PASS'. C01 sheet attribution wording (applied as r2c); C02 keep the installer's own output or run a read-only pip check, if the owner approves; C03 no further change.

Q10. What is the one production results source, its exact host, and who may contact it?
A10. Lotterywest-GOV: https on exactly www.lotterywest.wa.gov.au (results-search page), and only through the owner's approved, reviewed tools run by the owner. No AI chat or Claude Code contacts any lottery website; never oz.lotterywest.com, The Lott, an API, a scraper or a results search.

Q11. At this checkpoint, which of these has been authorised or run: the Windows POC rerun, the updater's offline self-test, the official-page check, the backup confirmation, any Approval 1-4?
A11. None. All are pending, each needing its own owner go; D1-D7 are also undecided. Source: readiness sheet r2c, register v0.29, OWNER_REMINDERS R-026.

Q12. What does 'sealed' mean in this project now, and how should the holdouts' present state be described? Until when is the code and Python environment frozen?
A12. 'Sealed' means only that a game's MODE_H_SEALED marker exists (scored and closed). The holdouts are now 'unopened' (no opening record). The freeze lasts from the first Approval 1 until BOTH games are sealed: no change under src/, root .bat, requirements, the venv or Python, no MHUP-B install, no installer run.
