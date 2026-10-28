# outbox - reports from the Claude Code local runner

Claude Code writes one report per task here, `REPORT_<id>.md`, and commits it with `tools\cc_clone.py commit-report --task <id>`. The project owner pushes; the Claude web chat then reads the report from GitHub.

## Report format

Plain ASCII Markdown. Copy outputs exactly, in fenced blocks; never shorten or reword a check's output unless the task file says which part to keep.

```text
# REPORT_<id> - <task title>

RESULT: PASS | STOP at step <n> | NOT STARTED (<reason>)

- Task file: inbox/TASK_<id>.md at main-repository commit <full hash>
- Run by: Claude Code (local runner), <date and time, with time zone>
- Owner options used: <as given by the project owner, or "defaults">
- Machine: <Windows version>; Python <version> at <venv python path>

## Steps

| Step | What | Exit code | Result line |
|---|---|---|---|
| 1 | ... | 0 | ... PASS ... |

## Outputs

### Step 1
(the command, exactly as run)
(its full output, in a fenced block)

## Clean-up
(the remove command's output; or why the task clone was left in place)

## Deviations
(any way the run differed from the task file, or "None")

## Observations
(optional: plain facts only, such as a warning that was printed; no opinions or suggestions)
```

Never put in a report: an outcome of any draw, the contents of any data file, personal details, or anything from outside this repository.
