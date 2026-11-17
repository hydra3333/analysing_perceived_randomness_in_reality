### L4. The league table

- **Sources** (Sup 4), each through its own read-only adapter that returns the same small row shape (key, hits, class,
  source identity, exposure flag): (a) the weekly score ledger; (b) the development score ledgers of the canonical
  attempts listed in `LEAGUE_SOURCES_<GAME>.json`; (c) the sealed Mode H ledger, shown and never summed, read only if
  its SHA-256 equals the one in its `SCORE_COMPLETE` record.
- **`LEAGUE_SOURCES_<GAME>.json` is one small tracked file** (Sup v0.8 4 rule 5; EX_223 C03), at
  `results/method_rankings/<GAME>/league/`. It lists the canonical development attempts, each by attempt identity,
  batch, kind, the digest of its score ledger and the keys' scope. There is no chain of versions: Git keeps its
  history, and every published table names the file's digest and the exact sources it used. It is written only by
  the admission step below, by an atomic replace of the whole file. The owner never edits it.
- **Admission is deterministic and part of the job that made the attempt** (Sup v0.8 4 rule 2A). `admit` adds a
  routine-fill attempt, or a report attempt over a version-1 batch, only if its report completed and none of its keys
  is already supplied by a canonical source or by the weekly score ledger. Otherwise it refuses, names the first conflicting key, and changes nothing. An
  exploratory attempt is never admitted. So the canonical score of a key is the first one admitted, never the newest
  or the best. The two existing attempts (`rr-4be324ab...` for Oz Lotto, `rr-97bb4861...` for Powerball) are admitted
  the same way at the first use after the install. Replacing a canonical source is not provided: it would be a
  reviewed, named change on the owner's decision.
- **The one-score rule:** key (game, method, revision, variant, target, barrel, TOP or WORST); the scoring policy is not
  in the key. Two canonical sources with the same key and no named selection: refuse, naming the key. A correction
  chain that branches, cycles or has two heads: refuse. A listed source absent or failing its identity: "not
  available: <source>" for the affected variants, never a partial total shown as a total.
- **The table** (Sup 3): every released variant; `NO_SCORES`; `LOW_N` under 30; all scored draws (no P value); forward
  only with the witness-verified count beside it; last 10; the second table by kind with "Mode H as sealed"; WORST;
  the Powerball barrel; divisions; revision, release date, first and last scored target, missing and failed counts;
  the order by hits above chance per draw as an exact fraction, ties by identity; the fixed header sentences; the
  exposure flags HX-1 and HX-2 wherever a flagged draw is scored, from the recorded source, changing no figure
  (EX_223 CP-Q8).
- **Publishing, made crash-consistent** (Sup v0.8 5.1; EX_223 B02). One publication has one identity: game, version,
  latest draw and time stamp, which are its file names.
  1. Build both members' bytes in memory and check them.
  2. Create the publication's manifest in the archive, create-only: the identity; both members' digests; and every
     input pinned so the bytes can be rebuilt exactly (the source file's digest and entries, each ledger's verified
     length and digest, the roster with release dates).
  3. Create the two archive members, create-only.
  4. Append the `WEEKLY_TABLE` search-log row, naming the manifest. **The row is written last, so a row always points
     at a complete, verified set.**
  5. Refresh `current`: new copies under temporary names, verified against the archive; a `CURRENT_COPY_INCOMPLETE`
     notice placed; the old copies replaced; the notice removed last.
  Every `publish` and `repair` first looks for a manifest with no row. It rebuilds that publication from the manifest's
  pinned inputs; if the bytes equal the manifest's digests it creates whatever member is missing and appends the row
  (the same bytes, the same identity). If they cannot be rebuilt identically it writes a create-only
  `PUBLICATION_INCOMPLETE` note beside the manifest, reports it, and never logs that publication. Nothing in the
  archive is overwritten or deleted, no logged path ever lacks its files, and version numbers come from the manifests,
  so none is reused. A failed `current` copy is repaired from the archive.
- **Who starts and who writes** (Sup v0.8 4 rule 4; EX_223 C01). A publication is started only by `Method_League_Table.py
  publish`, which the weekly and development sequencers run and the owner may run on its own. Whoever starts it, the
  same writer runs the same five steps, so no publication can exist without its row. `league_sources.py` and
  `league_table.py` open nothing for writing (a static test); `league_publish.py` is the only writer of the table
  files, the manifest, the `WEEKLY_TABLE` row and the source file. A test drives both entry points.
- **Exploratory attempts** appear only in a separate, labelled comparison (by named attempt, beside the canonical
  figure for the same keys), never in a canonical column or total.
- **Gates:** each refusal and each degraded case of Sup 4 once; the adapters on writer-made records and on the real
  committed ones (section 8); an interruption before and after every durable step of a publication and of the
  `current` copy (section 9); a manifest whose inputs have changed is marked incomplete, not finished wrongly;
  admission refused on an overlapping key, with the file byte-identical; a repeated attempt for a covered key never
  counted; the history report recomputes nothing; every reconstruction row carries its label and the "released at
  that date" column.

