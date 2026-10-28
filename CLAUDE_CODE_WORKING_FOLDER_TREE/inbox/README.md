# inbox - task files for the Claude Code local runner

Only the Claude web chat writes task files here, and they reach the owner's machine by `git pull`. Claude Code never edits this folder.

**Name:** `TASK_<id>.md`, where `<id>` is `T` and three digits (`T001`, `T002`, ...). The report for a task is `outbox\REPORT_<id>.md`, and its task clone (if any) is `scratch\<id>\`.

**Every task file has these parts:**
1. **Header:** task ID, date, author (the Claude web chat), and what the task is for, in one or two sentences.
2. **Owner options:** anything the project owner may choose when starting the task, with the default (for example "T12: not run unless the owner says `with T12`").
3. **Paths:** the full paths the steps use, written out once.
4. **Steps:** numbered. Each step gives the exact command, what it should print (the PASS line), and what to do on anything else (normally: STOP, go to the clean-up step).
5. **Clean-up:** removing the task clone, which happens whether the task passed or stopped.
6. **Report:** what the report must contain beyond the standard format in `outbox\README.md`.
7. **Finish:** commit the report with `tools\cc_clone.py commit-report`, then tell the project owner the result line and "please push".

A task file never asks for anything the rulebook (`..\CLAUDE.md`) forbids. If one seems to, Claude Code stops and asks the project owner.
