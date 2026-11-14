# H-2 v2 full handover - proposed owner installation procedure (DRAFT, NOT A GO)

Do not execute these steps until: (1) Claude has fact-checked EX_172 and this complete H-2 v2; (2) the owner has explicitly RATIFIED/approved the final document bytes; (3) H-1 v2, H-2 v2 and register v0.29 have been finalised to agree; (4) Claude or ChatGPT has supplied a fresh complete final hash/manifest and expected file list. This candidate uses a CANDIDATE status and will require finalisation before installation.

Recommended: one *combined documentation-only* owner installation for five files, so both full handovers and register have coherent pointers before the first Mode H Approval 1. Claude should prepare a single exact-path manifest and simple owner-run commands/verification for that final combined round. The two-file overlay included here is the H-2-only subset for inspection; it is not an invitation to install separately without approval.

The two H-2 target paths are exactly:
- doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v2.md
- doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v2_introductory_blurb.md

The *other* three files for the combined round (Claude's, once finalised and approved) are:
- doc/HANDOVER/Claude_Primary_Handover_H1_v2.md
- doc/HANDOVER/Claude_Primary_Handover_H1_v2_introductory_blurb.md
- doc/RATIFICATION_REGISTER_v0_29.md

At the later owner-approved gate, commands should follow this general order: confirm clean tree and proper current main; fetch/pull BEFORE any Mode H freeze; verify source ZIP hashes; extract/copy only the five named paths; check exact byte identities of the working copies (taking CRLF differences into account); stage only five named paths; inspect `git diff --cached --name-only` and file content; commit; check the committed Git blobs against the final manifest; push only after the committed check PASS; have Claude independently verify against GitHub. Any unexpected path, hash, status, dependency or source_data/results modification is STOP; do not improvise a reset or repair.

Never change source code, results, Python venv, program launchers or holdout flags during a documentation install. This is NOT approval of D1-D7, any preflight execution, Mode H manifest/open/update/plan/score or MHUP-B work. If the first Mode H Approval 1 has happened by install time, STOP and reassess the frozen-path and owner-Git constraints instead of applying these generic instructions.
