## 6. Production's Python environment (D6; the owner's decision H1, entry 113; EX_252 sections 3 and 4; entry 116)

- **Built by the owner, his way, as on E:.** `create_venv.bat`, then `install_upgrade_dependencies_into_venv.bat`, run
  in `G:\a_p_r_i_r` (both are in the release, with the two activate scripts they call). That step needs the internet,
  as it does on E: today. **v0.2's lock file and wheel folder are withdrawn.**
- **It is in every snapshot** (section 7), so a restore brings back the very environment that was running. Nothing is
  rebuilt at a restore.
- **One rule: verified before use.** After any build or change the owner runs `update` (the same command; **a
  verification-only `update` on the release already deployed is allowed** and changes no code). It finds that the
  environment is not the verified one and: (1) removes any older `ENVIRONMENT_VERIFIED.json` first; (2) runs the
  existing environment inventory (`environment_inventory()` in `src/methods/_common/closure.py`), which refuses an
  orphan file and gives the environment's full digest; (3) runs the whole suite in a temporary export of the release
  commit with production's Python; (4) only on a pass writes `.venv\ENVIRONMENT_VERIFIED.json` (that full digest, the
  installed distributions and versions, the release, the time) and a deployment-log line, and takes the
  POST-deployment snapshot. **A failed verification leaves no marker.** This is the "verification command".
- **How an unverified environment is kept from real work: two checks, each stated for what it is.**
  1. *At every launch, a cheap first gate:* the production guard (section 10) requires the marker file and requires the
     installed distributions (names and versions: one directory listing) to equal its list. This catches a deleted and
     rebuilt `.venv` and any upgrade that changes a version. **It does not catch a reinstall of the same version or a
     changed file inside a package,** and is not described as doing so.
  2. *At every job boundary, the full identity:* the weekly and development sequencers, and the deploy tool's `update`
     and `check`, compute the full inventory digest and refuse if it is not the marker's. (The weekly session already
     computes this digest when it opens a session, so this adds a comparison, not a scan.)
  3. *The owner's script removes the marker before it changes anything* (the owner's yes, entry 116 item 5): one line
     added to `install_upgrade_dependencies_into_venv.bat`, in its installing modes only (its `VERIFY` mode reads only).
  **What is left, stated:** `pip` typed by hand, reinstalling the same versions, followed by a single owner command
  typed before any job or `update`. The next job boundary refuses.
- **W-23 is unchanged (EX_252 section 4; the owner, entry 116 item 4).** H1 changes how the environment is built. It
  does not change who must look first. Every dependency upgrade keeps the always-review rule (H-1 v7r1 sections 1.5
  and 5.4), in this order, each time:
  1. The owner says what he means to upgrade; the reviewer assesses it; the owner gives that upgrade's go.
  2. The E: clone is rebuilt. The evidence H-1 5.4 names is produced there by a Claude Code task: the offline suites,
     the numerical and N-1 tests, the W-suite including W-23, and every E_1 golden, with no golden recalibrated. Any
     exclusion is named and needs the owner's explicit acceptance.
  3. The reviewer sees that report.
  4. Production: `Run_Production_Snapshot.bat` (the "before" snapshot); the rebuild; `update` (the same evidence with
     production's own Python, the marker, the "after" snapshot).
  5. Only then a real job. Until step 4 passes the guard refuses anyway.
  T024's acceptance of 14 November 2026 covered that one change and is no waiver. The owner may revise W-23 after a
  review; this note does not.
- **At `init`:** after the data and the code are in place, `init` stops and asks the owner to build the environment
  with his two scripts; the same `init` command typed again goes on with the verification.
- **What this gives up, stated plainly.** Production's package versions are whatever `pip` resolves that day and may
  differ from E:'s. The evidence is the suite passing in production's own environment, and the snapshot holds the
  exact files. All of the installer's 39 packages are installed, not only the five this project imports.
- **An old snapshot after a major Python change** may hold an environment that no longer starts, because a Windows
  environment depends on the base Python being where it was. The restore says so and does not call it ready
  (section 8); the fix is the same rebuild and `update`.

**Alternatives.** (1) The pinned lock and wheel folder of v0.2: reproducible and offline, but machinery the owner
would work around; he chose H1. (2) No marker, the rule kept by procedure only: the reviewer judged the marker worth
keeping (EX_252 section 3). (3) The full digest at every launch: exact, but a scan of the whole environment before
every inner method run, for a case the job boundary already catches.

