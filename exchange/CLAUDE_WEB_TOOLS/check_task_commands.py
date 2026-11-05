"""Check a Claude Code task file's commands against the repository's .claude/settings.json Bash deny list, before the
task is committed (Claude web chat, 5 November 2026, after TASK_T019 stopped at a denied command line).
Every non-blank line inside a ``` fence is taken as one command and matched against every Bash(...) deny pattern
with shell-style wildcards over the whole command text, as the runner's permission layer matches it.
Usage: python3 -I check_task_commands.py <repo> <task file> ...   Prints PASS, or STOP with each denied line."""
import fnmatch, json, sys
from pathlib import Path

repo = Path(sys.argv[1])
deny = [d[5:-1] for d in json.loads((repo / '.claude' / 'settings.json').read_text(encoding='utf-8'))['permissions']['deny']
        if d.startswith('Bash(') and d.endswith(')')]
bad = 0
for name in sys.argv[2:]:
    text = Path(name).read_bytes().decode('ascii').replace('\r\n', '\n')
    inblock, n = False, 0
    for i, line in enumerate(text.split('\n'), 1):
        if line.startswith('```'):
            inblock = not inblock
            continue
        if inblock and line.strip():
            n += 1
            hits = [d for d in deny if fnmatch.fnmatchcase(line.strip(), d)]
            if hits:
                bad += 1
                print(f'{name}:{i}: denied by {hits}: {line.strip()[:120]}')
    print(f'{name}: {n} command line(s) checked')
print('STOP: denied command lines found' if bad else 'PASS: no command line matches a Bash deny pattern')
sys.exit(1 if bad else 0)
