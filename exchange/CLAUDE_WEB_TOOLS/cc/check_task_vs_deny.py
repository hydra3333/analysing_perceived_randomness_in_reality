"""Check every command line in a TASK file's code blocks against .claude/settings.json's Bash deny patterns.
Usage: check_task_vs_deny.py SETTINGS TASK  (exit 1 on any match)"""
import fnmatch, json, re, sys
deny = [d[5:-1] for d in json.load(open(sys.argv[1]))['permissions']['deny'] if d.startswith('Bash(')]
text = open(sys.argv[2], encoding='ascii').read().replace('\r\n', '\n')
cmds = [l for block in re.findall(r'```\n(.*?)```', text, re.S) for l in block.splitlines() if l.strip()]
bad = [(c, p) for c in cmds for p in deny if fnmatch.fnmatchcase(c, p)]
for c, p in bad:
    print('DENIED', p, '::', c[:160])
print(f'{len(cmds)} command lines, {len(deny)} Bash deny patterns, {len(bad)} matches')
sys.exit(1 if bad else 0)
