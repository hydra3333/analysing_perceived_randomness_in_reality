# Claude independent research - historical-results sources for Powerball and Oz Lotto (v2)

**Reviewer:** Claude (independent reviewer)
**Date:** 24 October 2026 (Adelaide)
**Supersedes:** v1 entirely. v1's statements that Lotterywest's robots policy refused access and that The Lott's terms were unknown were **wrong or incomplete**. Both were checked directly in a real browser for v2 (section 2).
**Responds to:** "Package 2 - Independent research: historical-results sources for Powerball AND Oz Lotto".
**Repository baseline inspected:** `057fd8c618c00d162324149e949fc71ab72ca3ce`.
**Status:** RESEARCH ONLY. No code changes, no scraping, no dataset assembly, no scientific analysis. Claude is not a lawyer; the terms readings below are plain-English readings, not legal advice.

**Evidence labels:** VERIFIED (checked directly), INFERRED (reasoned), UNRESOLVED.

**Data handling.** Checks on The Lott data used an already-published third-party JSONL copy (GitHub `nwbort/ozlot`), read only:

- **Powerball:** compared only on training draws 1144-1577. Holdout 1578-1587 and draw 1588 were excluded.
- **Oz Lotto:** structure only, apart from one early-era draw (1474), which was compared between publishers by SHA-256 of the number sequences, not by printing the numbers. Draw 1474 is far below any possible Oz Lotto holdout.

No ball numbers appear in this document.

---

## 1. Short answer

- **Lotterywest is a practical common official source for both games.**
  - It is the official WA operator and publishes the same national draws.
  - Its `robots.txt` **allows all crawling** (VERIFIED).
  - Its per-draw pages `https://www.oz.lotterywest.com/{powerball|oz-lotto}/results/draw/N` exist for both games. They have a "search past draw results by draw number" box, and the Oz Lotto pages label **"Main Numbers"** and **"Supplementary"** separately (VERIFIED for draw 1474).
  - Its Oz Lotto 1474 sequences (7 main and 3 supplementary) match The Lott's exactly, and are not in ascending order (VERIFIED by hash). So both official publishers present the same (drawn) order.
- **The Lott must not be used for automated retrieval.** The Lottery Corporation's Terms of Use (they cover thelott.com) allow content to be downloaded and viewed only "using an industry-standard web browser... for your personal, non-commercial use only". They prohibit "Any reproduction or redistribution... of the Content", including copying it "to any other server, location or support for publication". Scraping its API or website, or republishing Lott-sourced data in a public repository, conflicts with that.
- **Recommendation:**
  - **Keep ChatGPT's preliminary choice of Lotterywest as the Oz Lotto primary.**
  - Use **lottodraw.com.au** (server-rendered, both games, permissive in practice) as an independent second publisher for verification.
  - **Keep the existing Powerball pipeline and snapshot unchanged.** It already uses Lotterywest per-draw pages for drawn order, so Lotterywest is effectively the common official source for both games.
  - Build one shared framework with per-(source, game) adapters.

## 2. Access rights and terms (checked in a real browser, 24 Oct)

| Item | Finding | Status |
|---|---|---|
| `https://www.oz.lotterywest.com/robots.txt` | `User-agent: *` / `Disallow:` (empty), plus a sitemap. **Everything allowed.** v1's "robots refused" was the research fetcher's own policy, not the site's. | VERIFIED |
| `https://www.lotterywest.wa.gov.au/robots.txt` | `User-agent: *` / `Allow: /`. | VERIFIED |
| What oz.lotterywest.com is | An online platform operated by **Jumbo Interactive on behalf of Lotterywest** (Lotterywest FAQ "What is oz.lotterywest.com"). | VERIFIED |
| oz.lotterywest.com Terms and Conditions | These are the **Lotterywest Membership Terms and Conditions** (effective 23 April 2026), covering accounts and entries. No clause was found on robots, scraping, automated access, data mining, or copying or reproducing content. | VERIFIED (keyword search of the full page) |
| lotterywest.wa.gov.au legal information | Only "All contents copyright (c) Lotterywest. All rights reserved." Nothing on automated access. Game rules prevail over website information. | VERIFIED |
| `https://www.thelott.com/robots.txt` | Not present (the site returns its 404 page). | VERIFIED |
| The Lottery Corporation Terms of Use (linked as "Terms of Use" from thelott.com; they cover thelott.com, thelotterycorporation.com, keno.com.au, retailersweb.thelott.com; effective 9 Nov 2023) | s4: personal licence to view; "Any reproduction or redistribution of the Website, our Apps or the Content is prohibited... you must not copy the Content to any other server, location or support for publication, reproduction or distribution"; "You may, using an industry-standard web browser, download and view the Content for your personal, non-commercial use only." s5: no "attempt to gain unauthorised access". s11: no hyperlinks to any page without prior written permission. | VERIFIED |
| The Lott's results API (`data.api.thelott.com`) | Undocumented, Akamai-protected; the only known scraper imitates a browser. Combined with the browser-only, no-redistribution terms: **do not use**. | VERIFIED (terms); INFERRED (application) |

**Public repository caution:** the project's GitHub repository is public. Do not commit data obtained from The Lott.

- **Lotterywest:** asserts copyright in its "contents". Bare draw results are facts, and Australian law generally gives facts and compilations of facts weak copyright protection. Even so, the owner should decide consciously whether committed source CSVs stay public.
- **The existing Powerball CSVs** came from powerball.net and Lotterywest, not The Lott.

## 3. Candidate sources compared

| Source | Both games? | Official? | Coverage | Fields / order | Access | Assessment |
|---|---|---|---|---|---|---|
| **Lotterywest** (oz.lotterywest.com, run by Jumbo for Lotterywest) | **Yes** | **Yes** (WA operator; bloc partner) | Per-draw pages by draw number. Powerball back to at least 1144 (existing scraper); Oz Lotto 1474 present | "Main Numbers" / "Supplementary" labelled (Oz Lotto); date and time shown; sequence matches The Lott's (drawn order) | Robots allow all; terms silent on automation; one page per draw; the existing scraper parses its server-rendered HTML | **Recommended common official primary** |
| **The Lott** (The Lottery Corporation) | Yes | Yes (conducts draws) | Full history | Labelled primary/secondary; drawn order | Terms: browser-only, personal, no reproduction; bot-protected API | **Not for automated use**; manual browser spot checks for personal verification are fine |
| **lottodraw.com.au** | Yes | No ("not affiliated with The Lott or Lotterywest") | Yearly archives for both games; per-draw pages | Draw pages label "Winning numbers" / "Supps"; non-ascending order (INFERRED drawn) | Server-rendered HTML; a few pages per year | **Recommended independent verifier** (archive lagged by about 2 draws when checked) |
| **powerball.net** (current Powerball primary) | Powerball only | No | 2018+ archive by year | Sorted numbers (no drawn order) | `robots.txt` allows all | Keep for Powerball as now; cannot serve Oz Lotto |
| ozlotteries.com (Jumbo reseller) | Yes | Reseller | Per-draw pages | UNRESOLVED | Not retrievable by the research fetcher | Not needed |
| BeatLottery | Oz Lotto only | No | 1994+ | No draw numbers; CSV behind login | Login | Unsuitable |

**Brand independence:**

- **SA Lotteries** is operated by Tatts Lotteries SA (master agent since 2012) under The Lott, so its results are The Lott's dataset.
- **Lotterywest** is a separate organisation and publisher of the same national draws ("The Lott and Lotterywest operate as a bloc to jointly conduct the national games").
- **lottodraw and powerball.net** don't name their upstream source (INFERRED to derive from an official publication).
- Lotterywest versus lottodraw is therefore an independent **publication** check, not an independent observation of the draw.

## 4. Coverage and data accuracy (bounded checks)

- **Powerball training draws 1144-1577 (434 draws).** The Lott's sets + Powerball match the repository history CSV (powerball.net) in **434/434**. The Lott's primary sequence matches the repository's Lotterywest drawn-order CSV in **434/434**. Three publishers agree, which independently confirms the accepted snapshot (VERIFIED).
- **Oz Lotto era 1474..1705 (The Lott copy).** Every date equals the derived date 2022-05-17 + 7 x offset. Every draw has 7 + 3 distinct numbers in 1..47. Draws 1472-1473 show the old format (2 supplementaries, 45 balls), which confirms the 1474 era start in operator data (VERIFIED).
- **Oz Lotto 1474, Lotterywest vs The Lott.** Main sequence, main set and supplementary sequence are identical by SHA-256 (VERIFIED).
- **Completeness risk.** The third-party Lott copy lacked Powerball 1584 and Oz Lotto 1701-1702. Any source can have gaps, so consecutive numbering must be a hard structural check.
- **Draw time is inconsistent.** The Lott's live-draws page says "approximately 8:30pm AEST (9:30pm AEDT)". Lotterywest's Oz Lotto 1474 page shows "17 May 2022 8:00 pm", with no timezone. The profiles' nominal draw time stays **UNRESOLVED**. Use the closing time or a conservative cutoff for prospective-publication deadlines, not the display time.

## 5. Is a common source genuinely practical?

**Yes: Lotterywest.**

- It is official and serves both games with per-draw URLs addressed by draw number.
- Its fields are labelled, and it shows drawn order.
- Its robots policy permits crawling and its terms do not forbid automation.
- The existing Powerball pipeline already depends on it.

**Costs and risks:**

- **One request per draw:** about 444 for Powerball and 230+ for Oz Lotto on a full rebuild, with rate limiting. Incremental updates are only a few requests.
- **Operator change:** the platform is operated by Jumbo for Lotterywest, so layout and contract changes are possible.
- **Correlated errors:** any single official publisher can carry them, so independent verification is still needed (lottodraw for both games; powerball.net also for Powerball).

## 6. Recommended strategy (C with Lotterywest as the common official primary)

| Game | Primary | Independent verification | Notes |
|---|---|---|---|
| Powerball | **Unchanged:** existing accepted snapshot; existing pipeline (powerball.net archive + Lotterywest per-draw drawn order) | Already two publishers; optionally lottodraw | **No migration.** Any future snapshot must reproduce 1144-1587 content exactly (e.g. the 1577 U-view digest `d47fbbd6...4339`). |
| Oz Lotto | **Lotterywest per-draw pages** (keep ChatGPT's preliminary choice) | lottodraw.com.au yearly archives, plus per-draw pages where needed | The first scrape stays a separately gated Package 3 step. |

- **Do not use The Lott for automated retrieval or as a stored data source** (terms).
- Manual browser checks on thelott.com by the owner for personal verification remain fine.

## 7. Proposed Package 2 scraper changes

- **Shared framework:**
  - polite fetch: honest project User-Agent, rate limit and backoff, robots respected;
  - raw response archive with SHA-256;
  - per-(source, game) parsers;
  - profile-driven structural validation;
  - create-only dated snapshots;
  - a separate acceptance step;
  - source identity, URL and retrieval UTC time in raw provenance.
- **Lotterywest Oz Lotto adapter:** parse "Main Numbers" (7) and "Supplementary" (3) by their labels. Record the page's date and time string as provenance only, and drawn order with the label `SOURCE_ORDER_UNVERIFIED`. Upgrade the label to `DRAWN_ORDER_VERIFIED` only after a cross-publisher agreement check.
- **Hard checks:**
  - **Completeness:** consecutive draw numbers from 1474 to the snapshot end.
  - **Era:** 47 balls, 3 supplementaries.
  - **Derived dates:** date anomalies recorded only; they block E_14/E_54 only.
- **A separate cross-source verification command** (Lotterywest vs lottodraw). Its output is bounded: draw number, field, pass/fail, never values.
- **No adapter may impersonate a browser, bypass bot protection, or use The Lott's API.**
- **Powerball scraper:** fix only its output location, as planned.

## 8. Lotterywest / SA equivalence (secondary question)

- **Same draws, verified by data.** Powerball: Lotterywest's per-draw data and The Lott's agree on all 434 training draws checked, including drawn order. Oz Lotto: draw 1474 is identical across Lotterywest and The Lott (main, supplementaries, order). The draw-number identity is shared.
- **SA Lotteries is The Lott's dataset.** Lotterywest is a separate publisher of the same national draw, a useful verifier but not an independent observation.

## 9. Outstanding questions

1. Owner decision: whether committed source snapshots should stay in the public repository, given Lotterywest's copyright notice. Results facts carry weak protection, but it is the owner's call.
2. Nominal draw time: Lotterywest shows 8:00 pm with no timezone; The Lott says about 8:30pm AEST. Resolve before FINAL deadlines are fixed; use the closing time meanwhile.
3. Confirm at the first gated scrape that Lotterywest Oz Lotto pages are server-rendered HTML (as its Powerball pages are for the existing scraper) and complete from 1474.
4. A periodic re-check that Lotterywest's robots policy and terms stay permissive. Record the robots.txt hash in provenance at each scrape.

## Sources

- oz.lotterywest.com robots.txt and Terms and Conditions (browser, 24 Oct 2026): https://www.oz.lotterywest.com/robots.txt ; https://www.oz.lotterywest.com/about/terms-and-conditions
- Lotterywest Oz Lotto draw 1474 page (structure only): https://www.oz.lotterywest.com/oz-lotto/results/draw/1474
- Lotterywest FAQ, "What is oz.lotterywest.com": https://www.lotterywest.wa.gov.au/faqs/playing-online/general/what-is-oz-lotterywest-com
- Lotterywest robots.txt and legal information: https://www.lotterywest.wa.gov.au/robots.txt ; https://www.lotterywest.wa.gov.au/legal/legal-information
- The Lottery Corporation Terms of Use (linked from thelott.com): https://www.thelotterycorporation.com/terms-of-use
- The Lott live draws page (broadcast time): https://www.thelott.com/promotions/live-lottery-draws
- Lotteries in Australia (bloc): https://en.wikipedia.org/wiki/Lotteries_in_Australia ; SA Lotteries (master agent): https://www.treasury.sa.gov.au/sa-lotteries
- Third-party Lott data (read only, for bounded checks): https://github.com/nwbort/ozlot
- lottodraw.com.au archives: https://lottodraw.com.au/oz-lotto/archive ; https://lottodraw.com.au/powerball/archive/2018
- powerball.net archive and robots.txt: https://www.powerball.net/australia/archive/2018 ; https://www.powerball.net/robots.txt

*End of research v2.*
