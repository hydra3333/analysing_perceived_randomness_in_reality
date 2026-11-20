5. **A snapshot is one ordinary `.zip` of the COMPLETE production folder,** its Python environment included; only two
   temporary control files are left out. It is written by Python's own `zipfile`, taken only when production is quiet,
   and checked twice before it counts (the archive read back; the files read again). It goes to
   `T:\a_p_r_i_r_backups`, named with the date and time. Every production job ends with one, `update` also takes one
   before it changes anything, and `Run_Production_Snapshot.bat` takes one whenever you like. A "snapshot due" file,
   written before a job's first write, makes the next job take a missed one first. If one cannot be made, every job
   goes on with a loud warning that stays until one is made (your decision; the risk is stated in section 7).
6. **A recovery kit** for each release: a small, separate, dated, hash-checked `.zip` on T: holding the restore tool,
   the release's hash list and plain instructions. An emergency restore runs from the kit with whatever Python is
   installed; it needs neither the E: clone nor a working production folder. `update` and `init` stop if the kit
   cannot be written to T:.
7. **Restore** is plain: verify the snapshot, check that no Python program is running on the PC, rename the old tree
   aside (kept), unpack the whole snapshot at `G:\a_p_r_i_r`, verify every file, and it is ready to run, environment
   and all. Then you work normally: the updater, then the weekly session, replay the missing draws one at a time from
   the draws before each. That is the same chronological process and valid research (EX_244; EX_248 section 1).
   Nothing is compared with the old tree, no timestamp proof is asked for, nothing stops. As the very last resort you
   can unzip a snapshot by hand; the kit's instructions say what to run afterwards.
8. **The formal OV-1 claim is kept apart, with no human choice.** A trace of the passed code (section 9) shows the one
   thing a restore changes: a draw that was counted before the restore can come back as "missed". The fix is one
   objective check in the recorder, fed by a small restore notice: such a draw makes the *registered formal claim*
   read "not established from draw T". Forecasting, scoring, league tables and the descriptive OV-1 view never wait
   for it and are never changed by it.
9. **A marker file** at the production root, checked with its path at every real-data launch, so nothing real starts
   in the E: clone or in a copied or set-aside folder. The proof-of-concept suite still runs where it does today.
10. **A stale orphan marker never blocks a restore for ever and is never copied back as a live block:** restart the PC
    (checked), a clean process check, and your typed acknowledgement (section 8).
11. **Production's Python environment is built your way,** with your own scripts, as on E:. After any build or change,
    one command verifies it (the whole test suite with production's own Python); until then no launcher runs.

Every choice put to you so far is confirmed and listed in section 15.

