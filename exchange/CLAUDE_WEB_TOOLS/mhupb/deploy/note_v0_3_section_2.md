## 2. The production folder and the backup folder

    G:\a_p_r_i_r\                    PRODUCTION. Everything here is in every snapshot, except the two files marked *.
      PRODUCTION_ROOT.json           the marker: schema, this folder's absolute path, the time it was made, the
                                     release it was made from. Written once, last, by init or restore.
      PRODUCTION_SETTINGS.json       the owner's settings: the backup folder. Plain JSON the owner may edit.
      Run_*.bat                      the launchers (release)
      create_venv.bat, install_upgrade_dependencies_into_venv.bat, activate_venv.bat, deactivate_venv.bat
                                     the owner's own environment scripts (release), used as on E: (section 6)
      src\                           the code (release), with the install records and the barrier P where they are today
      source_data\  results\  transitory_data\      data and records, exactly as on E: today
      production_records\            written only by the deploy tool and the snapshot code:
                                     RELEASE_<commit>.json (the hash list of each release deployed; create-only),
                                     DEPLOYMENT_LOG.jsonl (its last line names the current release),
                                     SNAPSHOT_LOG.jsonl, INIT_RECORD.json, RESTORE_<date>_<time>.json (and, beside
                                     it, the bytes of any orphan marker a restore set aside as evidence),
                                     * SNAPSHOT_DUE and * SNAPSHOT_IN_PROGRESS.lock (never in a snapshot)
      .venv\                         production's own Python environment, with ENVIRONMENT_VERIFIED.json (section 6)

    T:\a_p_r_i_r_backups\            BACKUPS. Nothing here is pruned by any tool. The owner copies this whole folder
                                     to his USB3 drives and the cloud himself; no tool does that.
      PRODUCTION_<date>_<time>_<JOB>.zip          a verified snapshot, with <same name>.zip.sha256 beside it
      DEPLOY_KIT_<date>_<time>_<release>.zip      a recovery kit (section 4.7), with its .sha256 beside it
      <anything>.partial             an unfinished file: NOT a backup
      the Python installer file      kept there by the owner (one file), in case Python itself must be put back

Not in production: `.git`, `tests/`, `doc/`, `exchange/`, `review/`, `archive/`, `GAIS/`, the runner's folder. No
installed program reads any of them (CODE-3's static rule already forbids `src/` to refer to `archive/`).

**What is where, in one line each.** Inside a snapshot: all of `G:\a_p_r_i_r`, the environment, the settings, the
marker and every record included. Separate on T:, never inside a snapshot: the recovery kits and the `.sha256`
files. For a restore the owner needs one snapshot, its matching kit and a Python installation; nothing from E: and
nothing from the internet.

**Alternative considered:** putting the settings in the marker (one file). Rejected: the marker is identity and is
never edited; the backup folder is a setting the owner may change (D9).

