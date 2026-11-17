# MHUP-B code plan - DRAFT v0.2 (for the reviewer's focused recheck, then the owner's ratification)

**Status: DRAFT v0.2, by the Claude web chat, 17 November 2026 (Adelaide). A plan only. It authorises nothing: no code,
package, task file, run, registration, re-forecast or install. No implementation code exists.** By the owner's
instruction (decision log entry 67), no code is written until this plan is complete and owner-ratified and he has then
given a specific go for code.

**What changed from v0.1.** The reviewer's review (EX_223, which supersedes EX_221 and EX_222: PASS WITH REQUIRED
CORRECTIONS) and the owner's directions on OD-1 to OD-6 (decision log entries 69 and 70) are applied. Section 1A says
where each point landed. v0.1 stays beside this file, and `PLAN_v0_1_TO_v0_2.diff` shows every changed line. The design
amendments the plan needs are in the supplement's next full edition,
`exchange/CLAUDE_WEB_TOOLS/mhupb/MHUPB_DESIGN_SUPPLEMENT_v0_8_AMENDMENT_CANDIDATE.md` ("Sup v0.8"), which goes to the same
recheck and the same ratification.

**Authorities it stands on:** the ratified design `doc/Predictive_Randomness_ModeH_Update_Prospective_Design_v0_1r7.md`
("Des") sections 6 and 7 and Appendices E to L; the ratified supplement
`doc/Predictive_Randomness_MHUPB_Design_Supplement_v0_7.md` ("Sup"; RAT-33), which governs until v0.8 is ratified;
register v0.31; H-1 v4; the approach of 16 November 2026 with EX_206's conditions; the working approach P0-P6 (decision
log entry 1); EX_213's code-round gates; EX_219's cautions C1 and C2; EX_223. Where this plan and those documents
differ, they govern, and the difference is a fault in this plan. Where the plan relies on an amendment of Sup v0.8, it
says "Sup v0.8".

**Base:** `main` at `cc665ce` or later. No file under `src/`, `tests/`, no root `.bat` and no `requirements.txt` has
changed since `cc0ab73` (checked with `git diff`); `.gitignore` changed at `cc665ce` (section 3). **Risk tier:** HIGH
(always-review subjects: N-1 boundaries, holdout access, freezing and publication, TOP/WORST readout, the evaluator and
scorer, launchers).

**Evidence with this plan** (folder `exchange/CLAUDE_WEB_TOOLS/mhupb/codeplan/`): the baseline suite summaries; the OV-1
numerical probe `ov1_lower_bound_probe.py` and its outputs; the census of the real score records (`score_census.py`
and its output). The probe is a plan-stage feasibility tool on invented data, not project code.

