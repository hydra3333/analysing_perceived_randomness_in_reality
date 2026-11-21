## 9. OV-1 after a restore: no special rule (EX_253; EX_255 E04; EX_258 section 3; EX_259 section 7)

- **The restored snapshot is the authority.** Its variants, its canonical lists and its prevailing OV-1 ledger come
  back as they were. The ordinary job fetches the results and catches up, draw by draw, with those variants. Each new
  line is computed by the standing rule (simplification design, section 7). There is no restore notice, no stop, no
  registration to lose, and **no qualification of any line because a restore happened** (owner).
- **The score after a restore may differ from the one that was lost,** and that is a truthful result, not a fault. It
  equals the lost one when the same variants compute the same forecasts from the same earlier draws in an environment
  that gives the same numbers. It differs if, for example, a variant had been installed after the snapshot (it is
  not there any more, so it does not count), or the environment computes differently. Nothing is put back to make the
  two agree.
- **A variant installed again later is a new installation,** by the owner's separate decision. Its lists start again;
  its history is refilled; it joins the prevailing score from its new `FORWARD_FROM` draw.
- **The claim's wording** is the fixed text of the simplification design, 7.4: conditional on fair draws and on
  nothing having been chosen in the light of a draw's result. The owner chooses a snapshot for its reliability,
  normally the latest good one; the software cannot check that, and does not pretend to.
- **The environment** is the snapshot's own, restored with it. It is not rebuilt, upgraded or pinned (section 6;
  entry 119). If it does not start, the restore reports NOT READY and the owner decides.
- No science input is ever taken from the set-aside tree or from the clone.
- The trace made for v0.2 (section 14) stays beside this note as the record of what the old rule did.

**Order of ratification.** This note is to be ratified with the simplification design or after it, not before.

