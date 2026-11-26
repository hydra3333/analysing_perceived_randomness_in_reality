# How a tree knows which tree it is: a proposal for discussion (v0.1)

**Date:** 26 November 2026. **Author:** the Claude web chat, at the owner's request (decision log entries 332 and 335).
**For:** the owner and the ChatGPT reviewer chat. **Status:** a discussion paper, not an EX message, not proposed for
ratification. Everything stays paused (entry 330). It becomes one section of the short scheme document if agreed.

## 1. The settings file, as the owner sketched it

One file of the same form in the root of every tree. Only the `role` line differs. Paths below are the ones
already decided (entry 181); DEV's backup folder is new and is a suggestion.

    [environment]
    role = QA

    [DEV]
    tree_root = E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality
    backup_root = T:\a_p_r_i_r_backups\DEV

    [QA]
    tree_root = T:\a_p_r_i_r
    backup_root = T:\a_p_r_i_r_backups\QA

    [PROD]
    tree_root = G:\a_p_r_i_r
    backup_root = T:\a_p_r_i_r_backups\PROD

Each tree's Python environment is the `.venv` folder inside it, so it needs no key. In DEV the file is already
ignored by Git, so a clone never carries it.

## 2. The proposal: four short rules

1. **A command works on the folder its own launcher lies in.** It never takes the folder to write in from the
   settings file. So `Run_Research.bat` in `T:\a_p_r_i_r` reads and writes `T:\a_p_r_i_r`, whatever any file says.
2. **Before it does anything, it checks that the folder is the tree the file says.** The `role` must be DEV, QA or
   PROD, and the `tree_root` of that role's section must be the folder the launcher lies in. If not, it stops and
   names both: "this folder is T:\a_p_r_i_r; the settings say role PROD at G:\a_p_r_i_r".
3. **Before it writes into another tree, it reads that tree's own settings file.** An install from DEV into QA
   looks in the folder DEV's file names for QA, and goes on only if a settings file lies there that says
   `role = QA` and passes rule 2 for itself. No settings file there means "not a tree": it stops. A new tree is made
   only by the one create step, into a folder that is absent or empty, and that step writes the file.
4. **When the file is read, three things about its paths are checked:** no two roles share a `tree_root`; no tree
   lies inside another; no backup folder lies inside its own tree.

And one habit: **no copy between trees ever copies the settings file.**

Paths are compared as Windows sees them (real, absolute, letter case ignored). That comparison code exists
already in the settings reader of slice A and can be kept as it is.

## 3. The holes I looked for

| The mistake | What happens |
|---|---|
| QA's file says `role = PROD` (a typing slip) | Rule 2 stops every command in QA. Even without rule 2, rule 1 keeps the writes in QA's own folder |
| The whole PROD folder is copied over QA by hand (the settings file with it) | The same: QA's file now says PROD at G:; rule 2 stops and says so. The owner puts the role line right |
| A backup of PROD is unpacked somewhere else to look at it | Its file says PROD at G:, but it lies elsewhere: rule 2 stops any command run there. Real PROD is never touched |
| A tree's folder is moved, renamed, or its drive letter changes | Rule 2 stops until the path in the file is brought up to date |
| DEV's file has QA and PROD at the same path, or QA's path is really PROD's | Rule 4 stops the first; rule 3 stops the second, because the file found there says PROD, not QA |
| DEV's file has an old path for QA | Rule 3: no tree's settings file lies there, or a different one does. It stops; nothing is created by accident |
| The T: drive is not connected | Rule 3: nothing lies there. It stops; it never makes a new tree where an old one should be |
| The backup folder is put inside the tree | Rule 4 stops it; otherwise every ZIP would hold all the earlier ZIPs |
| `role = prod` or `PRDO` | Not one of the three words: it stops and says which words are allowed |
| A copy of software from PROD into QA | The settings file is left out by name; if it were copied all the same, rule 2 catches it |

## 4. What it does not catch, said plainly

- **A consistent relabelling.** If someone edits both the role line and the paths so that the QA folder calls
  itself PROD at its own path, QA's file is self-consistent. Its own jobs still write only into its own folder
  (rule 1), so the real PROD is safe; and DEV's installs still go by DEV's file and rule 3.
- **The three files drifting apart.** Nothing keeps the copies in step. A tree only uses its own section and the
  sections of trees it writes into or copies from, and rule 3 turns a stale path into a refusal with a plain
  message, not into damage. I would not build a tool to keep them equal.
- **A destination whose settings file is lost.** It cannot be installed into until the owner puts the file back
  (by hand or from a backup).

## 5. One alternative I considered and do not recommend

The identity as a flag file in the tree's root (`I_AM_QA`), with the paths file identical everywhere and freely
copied. It matches the other flag files, but it gives no more safety than rules 1 to 3 (a hand copy of a whole
folder carries the flag just as it carries the settings file) and it adds a file. The owner's one-file layout is
simpler.

## 6. Questions

- **For the owner:** does this cover the holes you had in mind? If not, which one gets through? And is
  `T:\a_p_r_i_r_backups\DEV` right for DEV's backups?
- **For the reviewer:** is there a way for a command run in one tree to write into another that rules 1 to 3 do
  not stop? Is any of the four rules more than is needed?

END.
