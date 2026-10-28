# CLAUDE_CODE_WORKING_FOLDER_TREE - for the project owner

This folder lets Claude Code, in VS Code on your Windows machine, act as the project's **local runner**: it carries out task files written by the Claude web chat and reports back. It makes no design or code decisions. Its rulebook is `CLAUDE.md` in this folder.

| Item | What it is | Who writes it |
|---|---|---|
| `CLAUDE.md` | the rulebook Claude Code follows | the Claude web chat (or you) |
| `inbox\TASK_<id>.md` | one task, step by step | the Claude web chat |
| `outbox\REPORT_<id>.md` | what happened when the task ran | Claude Code |
| `tools\` | the helper programs the tasks use (task clones, checks) | the Claude web chat |
| `scratch\` | task clones; ignored by Git, never committed | Claude Code, via `tools\cc_clone.py` |
| `root_files\` | drafts of the two files that go at the repository root | the Claude web chat |

**Task clones.** A task that would change repository files works in `scratch\<id>\r`, a fresh clone from GitHub with its link to GitHub removed and a hook that refuses every push. Your own repository is never changed, except for Claude Code's report file in `outbox\`, which it commits (one file, checked) and you push.

## One-time setup (Windows CMD, repository root)

```bat
cd /d E:\SOFTWARE-Win11\powerball\analysing_perceived_randomness_in_reality
git pull --ff-only
copy CLAUDE_CODE_WORKING_FOLDER_TREE\root_files\CLAUDE.md CLAUDE.md
mkdir .claude
copy CLAUDE_CODE_WORKING_FOLDER_TREE\root_files\.claude\settings.json .claude\settings.json
git add CLAUDE.md .claude/settings.json
git status --short
git commit -m "Claude Code local runner: root CLAUDE.md pointer and .claude/settings.json"
git push
```

`git status --short` should show just two lines, `A  .claude/settings.json` and `A  CLAUDE.md`, apart from any files of your own that were already there.

Then close and reopen Claude Code in VS Code, so it reads the two new files. Optional checks inside Claude Code: `/memory` should list both CLAUDE.md files, and `/permissions` should list the deny rules.

What the two root files do:
- `CLAUDE.md` (root): a short pointer that loads the rulebook into every Claude Code session started in this repository.
- `.claude\settings.json`: rules enforced by Claude Code itself, not just by the model. It turns off web access; blocks pip, curl and similar; blocks running the coordinator, launchers and `.bat` files; blocks Git commands that change or push the repository (Claude Code uses the helper tools instead); blocks reading any `source_data`, `results` or `transitory_data` folder; blocks editing anything outside this folder, and the rulebook, tools and inbox inside it; and turns off the "bypass permissions" mode. These rules cover Claude Code's own tools and the shell commands it types; they do not police what a Python program does, which is why the rulebook and the checked helper tools matter as well.

## Each task

1. `git pull --ff-only` (this brings the new task file).
2. Start a new Claude Code conversation (or close and reopen Claude Code), so that it loads the rulebook as it now is; it reads `CLAUDE.md` only when a conversation starts.
3. In Claude Code, type: `Do inbox\TASK_T001.md` (the web chat tells you the task name and any options, such as `with T12`).
4. Claude Code asks before each command. Approve a command only if it is one of the task file's commands. If anything looks different, say no and tell the web chat.
5. When Claude Code says "please push": `git push`. Then tell the web chat the task's RESULT line; it reads the report from GitHub.

If `git status` ever shows `.claude/settings.local.json` (your personal "don't ask again" choices), do not commit it.
