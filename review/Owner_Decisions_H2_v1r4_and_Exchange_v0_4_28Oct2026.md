# Owner decisions - H-2 v1r4 ratification and exchange README v0.4 (28 October 2026)

**Recorded by:** Claude (primary designer and coder), from the project owner's explicit answers in the Claude chat, 28 October 2026 (Adelaide, UTC+10:30).
**Status:** an owner-decisions record, installed with DOC-4 as evidence. The next register edition records these decisions formally; until then this file and the DOC-4 install commit are the in-tree record. It authorises nothing beyond the two decisions below.

## 1. H-2 v1r4: OWNER-RATIFIED 28 October 2026

- **The document:** `doc/HANDOVER/ChatGPT_Reviewer_Handover_H2_v1r4.md`, Git-content SHA-256 (UTF-8, LF) `73b90ea348aea5fc337097a14ec4a8669258bc6cba55ce5a2485de26575f3f3a`. Author: the ChatGPT reviewer chat. It is installed by DOC-4 and replaces H-2 v1r3 for future reviewer roles. v1r3 (`a2fb5c641a6fa8010aa59ff811aeba23145703bd5c0d4e2dbd70ac2fb419edb1`) is kept as history.
- **Its review:** the one factual review, by Claude, in `exchange/EX_023_Claude.zip`; its message is stored as `review/Claude_Fact_Check_H2_v1r4_v1.md`. It made three documentary corrections, H2F-01..03, which the reviewer adopted in `exchange/EX_024_ChatGPT.zip` (H2-RD-01..03).
- **The rights block is unchanged:** the reviewer-rights region (from `## 2` up to `## 4`: R-1..R-11, T-05 and section 3.1, 7,676 bytes) is byte-identical to H-2 v1r3. Both chats checked this mechanically.
- **Its headers are historical:** its authoring-time status lines ("PENDING PROJECT-OWNER RATIFICATION/INSTALLATION", "This draft does not replace it") are historical, as with earlier handovers; this record and the install commit determine its status.
- **The history files installed with it, under `review/`:**
  - `ChatGPT_Reviewer_Handover_H2_v1r4_initial_draft.md`, the EX_022 draft;
  - `ChatGPT_Reviewer_Handover_H2_v1r4_fact_corrections.diff`, H2F-01..03;
  - `ChatGPT_Reviewer_Handover_H2_v1r3_to_v1r4.diff`, the exact predecessor diff;
  - `Independent_ChatGPT_EX_024_H2_v1r4_Final_Candidate.md`;
  - `Claude_Fact_Check_H2_v1r4_v1.md`.

  The EX messages are stored as LF copies, otherwise unchanged.

## 2. exchange/README.md v0.4: OWNER-DECIDED 28 October 2026

- **What it says:** EX message files stay US-ASCII with CRLF. An enclosed document that is, or derives from, a UTF-8 project file keeps its characters, in LF or CRLF, and its identity is the SHA-256 of its canonical LF bytes.
- **Where it is:** committed by Claude inside `exchange/` only, at `63c19e7515e02acc10af1a9c7a290acc73371b7e` (Git-content SHA-256 `b08d9e2b62daf1f435c5c02b8908e447c1bc790b28d1d92c2866f110846b2256`).
- **Why:** earlier enclosures were UTF-8: the register v0.9 candidates in EX_015, EX_017 and EX_019, and H-2 v1r4 in EX_022 and EX_024. Under v0.3 they were unflagged or flagged exceptions; v0.4 makes them conforming.
- **What it is not:** this is a protocol clarification only. Nothing in `exchange/` is ratified.

## 3. Unchanged

- **The order (DOC3-RD-09):** E1-ALIGN code follows this handover's installation, and still needs the owner's authorisation, its HIGH-tier review and the Windows acceptance run.
- **No permissions:** no run, test, data access, holdout, switch or allowlist change follows from these decisions.
