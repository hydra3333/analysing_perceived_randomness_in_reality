## 6. Production's Python environment (D6; the owner's decision H1, decision log entry 113)

- **Built by the owner, his way, as on E:.** `create_venv.bat`, then `install_upgrade_dependencies_into_venv.bat`, run
  in `G:\a_p_r_i_r` (both are in the release, with the two activate scripts they call). That step needs the internet,
  as it does on E: today. **v0.2's lock file and wheel folder are withdrawn.**
- **It is in every snapshot** (section 7), so a restore brings back the very environment that was running. Nothing is
  rebuilt at a restore.
- **One rule: verified before use.** After any build or change the owner runs `update` (the same command; with no new
  release it changes no code). It sees that the environment is not the verified one and: (1) runs the existing
  environment inventory, which refuses an orphan file; (2) runs the whole suite in a temporary export of the release
  commit with production's Python; (3) on a pass writes `.venv\ENVIRONMENT_VERIFIED.json` (the environment's digest,
  the installed distributions and versions, the release, the time) and a deployment-log line, and takes the
  POST-deployment snapshot. **This is the "verification command".**
- **Until then no launcher runs.** The production guard (section 10) requires that file, and requires the installed
  distributions (names and versions, read from the folder names in `site-packages`: one directory listing) to equal
  its list. A deleted and rebuilt `.venv` has no such file; an upgrade in place changes the list. Either way every
  real-data launcher refuses and says: run `update` to verify the environment.
- **The owner's procedure for an environment change** (a new Python, say), each time on his own go as a dependency
  change (W-23): in the E: clone first (rebuild; the suite by a Claude Code task, as T024 did). Then in production:
  `Run_Production_Snapshot.bat` (the "before" snapshot); rebuild; `update` (the verification and the "after" snapshot).
- **At `init`:** after the data and the code are in place, `init` stops and asks the owner to build the environment
  with his two scripts; the same `init` command typed again goes on with the verification.
- **What this gives up, stated plainly.** Production's package versions are whatever `pip` resolves that day and may
  differ from E:'s. The evidence is the suite passing in production's own environment, and the snapshot holds the
  exact files. All of the installer's 39 packages are installed, not only the five this project imports.
- **An old snapshot after a major Python change** may hold an environment that no longer starts, because a Windows
  environment depends on the base Python being where it was. The restore says so and does not call it ready
  (section 8); the fix is the same rebuild and `update`.

**Alternatives.** (1) The pinned lock and wheel folder of v0.2: reproducible and offline, but machinery the owner
would work around; he chose H1. (2) No `ENVIRONMENT_VERIFIED.json`, the rule kept by procedure only: simpler by one
small file and one directory listing per launch, but a real job on an untested environment would go unnoticed. I
recommend keeping the file; the reviewer may judge it unnecessary.

