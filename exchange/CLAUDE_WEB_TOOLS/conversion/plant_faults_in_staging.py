"""Workspace check: plant one fault at a time in the stage-and-refresh program and see that its tests catch it.
Usage:  python -B plant_faults_in_staging.py <tools folder> <python>"""
import subprocess, sys, pathlib
folder = pathlib.Path(sys.argv[1]); python = sys.argv[2]
file = folder / 'stage_and_refresh.py'
MUTATIONS = [
    ("            if plan['to_stage']:\n                stage_exactly(tree, plan['to_stage'])", "            if False:\n                stage_exactly(tree, plan['to_stage'])", 'the listed files not staged'),
    ("    return {fields[position].decode('utf-8') for position in range(0, len(fields) - 2, 3)\n            if fields[position + 2] == ATTRIBUTE_UNSET.encode('ascii')}", "    return set(paths)", 'the other project\'s files refreshed too'),
    ("            if rule.differ_in_line_endings_only((tree / path).read_bytes(), blob):\n                plan['to_refresh'][path] = tracked[path][1]", "            if True:\n                plan['to_refresh'][path] = tracked[path][1]", 'a file changed here overwritten with Git\'s bytes'),
    ("            note_refreshed(tree, sorted(plan['to_refresh']))", "            pass", 'Git not told of the rewritten working copies'),
    ("    shutil.copymode(full, temporary)\n", "", 'a rewritten file losing its permission bits'),
    ("            if typed.strip() != WORD_TO_GO_ON:", "            if False:", 'not waiting for the typed word'),
    ("        if not full.is_file() or conversion.sha256_of_file(full) != entry['sha256_after']:", "        if not full.is_file():", 'a listed file staged though not at its "after"'),
    ("        if look_only:\n            say('STAGE AND REFRESH - END - LOOKED ONLY", "        if False:\n            say('STAGE AND REFRESH - END - LOOKED ONLY", 'a look that goes on to change things'),
    ("        if plan['problems']:\n            raise Stopped(", "        if False:\n            raise Stopped(", 'findings not stopping the run'),
    ("        if path not in on_disk:\n            plan['problems'].append(", "        if False:\n            plan['problems'].append(", 'a missing tracked file not noticed'),
    ("        note_refreshed" if False else "    unstaged = [name.decode('utf-8') for name in git(tree, 'diff-files', '--name-only', '-z').split(b'\\0') if name]", "    unstaged = []", 'the proof not asking Git whether it sees an unstaged change'),
]
original = file.read_text(encoding='utf-8'); caught = 0
for old, new, what in MUTATIONS:
    if original.count(old) != 1:
        print('NOT APPLIED -', what, original.count(old)); continue
    file.write_text(original.replace(old, new), encoding='utf-8', newline='\n')
    try:
        run = subprocess.run([python, '-B', '-m', 'unittest', 'test_stage_and_refresh'], cwd=folder, capture_output=True, text=True)
    finally:
        file.write_text(original, encoding='utf-8', newline='\n')
    failed = run.returncode != 0; caught += failed
    print('CAUGHT' if failed else 'MISSED', '-', what)
print(caught, 'of', len(MUTATIONS), 'planted faults caught')
