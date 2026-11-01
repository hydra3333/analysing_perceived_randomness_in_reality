# Predictive Randomness - Holdout Exposure Record v0.3 (OWNER-RATIFIED)

**Status:** OWNER-RATIFIED 1 November 2026 with the snapshot documents (prepared by Claude; content reviewed in EX_117, EX_119 and EX_121). It supersedes v0.2 (`aec833fe...33e2`, OWNER-RATIFIED 26 October 2026 as the ratification register records, although its own header still reads CANDIDATE) and v0.1 (owner-ratified 26 October 2026; SHA-256 `a98064494444831b703587c48523dfb5e4b3c8aa66a3d00729ffcaa9d563c33b`).

This is a factual, value-free exposure record. It contains no outcome values, no computations, and no claims about experimental influence.

**Changes from v0.2:**
- items 1 to 6 are unchanged (v0.2's text);
- new: the owner's decision HX-1 (1 November 2026) on how Mode H treats the exposure, and what it means for the holdout draws named in item 1;
- new: the owner's decision HX-2 (1 November 2026) on the two later draws named in item 1.

The holdout (FINAL_HOLDOUT_10, R3 v0.5 section 6) is Powerball draws 1577-1586 and Oz Lotto draws 1694-1703. The quarantined range begins at those draws and includes every later draw.

1. On **25 October 2026**, a reviewer chat displayed published results for Powerball draws **1585-1588**.
2. Historical Powerball `*_20261021.csv` files contained draws now in the quarantined range. They were removed from the active working tree and remain recoverable in Git history. The owner/Claude-side development-master tools use a raw **first-field draw-number filter** before parsing any subsequent field (draw < 1577).
3. Git commit `9b78b8f` contained a saved results page showing recent quarantined draws. A later commit removed it from the active tree; it remains in Git history.
4. The results pages the owner saved from The Lott in October 2026 for the cross-checks also carried that site's latest-draw panel, which showed then-recent draws of both games in the quarantined range.
   - The pages were kept outside the repository; some were attached to the reviewer chat as files.
   - The Claude-side tools never parsed that panel.
   - Apart from items 1, 5 and 6, no values were displayed.
5. Ratified R1 v0.4 and Proposal v0.3/v0.4 quote the published results of Powerball draw **1587** (in the quarantined range) as drawn-order evidence.
   - These files remain in the repository; R1 is protected and unchanged.
   - Claude's consolidation reviews of 25-26 October displayed that Proposal paragraph in the reviewer chat **more than once**, in document comparisons.
   - No result values are reproduced here.
6. On **26 October 2026**, during ChatGPT's independent review of the Method Ranking Measures Proposal v0.2, a public web search for game rules returned an **unsolicited search-result preview** containing published results of draws in the quarantined range. ChatGPT reported that:
   - it did not open the results page;
   - it did not use any of those values in calculations, analysis or documents;
   - none were reproduced.

   The game and draw numbers concerned were not stated. No values are recorded here.


## The owner's decision HX-1 (1 November 2026)

**Question:** item 1 names Powerball draws 1585 and 1586, which are inside the Powerball holdout (1587 and 1588 are later, quarantined draws). How should Mode H treat them?

**Decided by the project owner:**
1. **The exposure stays on record** (this document).
2. **Mode H scores all 10 holdout draws for each game.** No holdout draw is dropped or replaced.
3. **Powerball draws 1585 and 1586 carry a flag** in Mode H's records and in its report: they were displayed by a reviewer chat on 25 October 2026, before Mode H. The flag text names this record. It changes no score and no measure: the flagged draws remain fully valid and counted.
4. **Until Mode H opens the holdout, all 10 draws of each game are treated as unseen.** Every rule stays in force: no display, quotation or computation with Powerball draw 1577 or later, or Oz Lotto draw 1694 or later, by any chat, tool or person acting for the project.

**What the decision does not settle:**
- Items 4 and 6 do not identify draw numbers, so no further draw is flagged on their account; the Mode H report states that they exist.
- Item 5 concerns draw 1587, which is outside the holdout; it gets no Mode H flag (see HX-2 for its catch-up score).
- How the flag is stored and printed is part of the Mode H design (with the Mode H store, which R3 leaves OPEN).

**Why:** the methods' code never received any of these values; only chats saw them. The flag lets every reader of Mode H's results see the residual risk that people designing or choosing methods were influenced, without discarding a fifth of the Powerball holdout.

## The owner's decision HX-2 (1 November 2026)

**Question:** item 1 also names Powerball draws 1587 and 1588. They are after the holdout. Should the holdout be extended to cover them, and how are they treated?

**Decided by the project owner:**
1. **The holdout is not extended.** It stays fixed at Powerball 1577-1586 and Oz Lotto 1694-1703; it never slides (R3 section 6).
2. **Powerball draws 1587 and 1588 are ordinary post-holdout draws.** When the weekly session's catch-up (decision MH-1) scores them, **those two catch-up scores carry the same exposure flag** as draws 1585 and 1586 carry in Mode H, naming this record. The flag changes no score and no measure: the flagged draws remain fully valid and are counted like any other draw (no gap, nothing excluded); the flag is information only.
3. **Until they are scored,** every rule for draws at or after Powerball 1577 applies to them unchanged.

**Interpretation:** this record documents exposure and historical file presence only. It must not be used as an input to method fitting, scoring, tuning or selection. No winning numbers are reproduced. Nothing here claims that any exposure did or did not influence the project.
