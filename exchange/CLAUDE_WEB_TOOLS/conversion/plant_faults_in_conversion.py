"""Workspace check: plant one fault at a time in the conversion program and see that its tests catch it."""
import subprocess, sys, pathlib
folder = pathlib.Path(sys.argv[1]); python = sys.argv[2]
file = folder / 'convert_to_file_form.py'
MUTATIONS = [
    ("            elif digest == entries[path]['sha256_before']:\n                survey.to_convert.append(path)\n            elif entries[path].get('delivered_by_package'):",
     "            elif True:\n                survey.to_convert.append(path)\n            elif entries[path].get('delivered_by_package'):", 'a third SHA-256 taken as "before"'),
    ("    if survey.awaiting_package:\n        raise ConversionStopped(", "    if False:\n        raise ConversionStopped(", 'a run without the package\'s files not stopped'),
    ("    for path in links:\n        survey.problems.append(", "    for path in []:\n        survey.problems.append(", 'a link met in the walk not reported'),
    ("        if linked:\n            raise ConversionStopped(", "        if False:\n            raise ConversionStopped(", 'a lock written through a linked control folder'),
    ("            return 'it holds a status other than ACTIVE'", "            return f'it says \"{line}\"'", 'a status file\'s content printed'),
    ("            return 'it records a withdrawal or an eligibility draw'", "            return f'it records \"{line}\"'", 'a recorded fact\'s content printed'),
    ("    problems = check_copy(copy, {**record['originals_converted'], **record['originals_removed']})",
     "    problems = check_copy(copy, {**{p: entries[p]['sha256_before'] for p in survey.to_convert}, **survey.to_remove})", 'the copy checked against what is still to do, not the first run\'s record'),
    ("        with HeldLock(tree / JOB_LOCK, rule), HeldLock(tree / UPDATER_LOCK, rule):", "        with HeldLock(tree / JOB_LOCK, rule):", 'the updater\'s lock not held'),
    ("        if typed.strip() != WORD_TO_REMOVE:", "        if False:", 'the removal not waiting for its word'),
    ("        if typed.strip() != WORD_TO_CONVERT:", "        if False:", 'the conversion not waiting for its word'),
    ("                if fault:\n                    survey.problems.append(f'{path}: {fault}. A status file", "                if False:\n                    survey.problems.append(f'{path}: {fault}. A status file", 'a status file with a recorded fact removed'),
    ("            if faults:\n                survey.problems.append(f'{path}: {faults[0].what}. The results files", "            if False:\n                survey.problems.append(f'{path}: {faults[0].what}. The results files", 'a results file not in its form passed'),
    ("    if survey.problems:\n        raise ConversionStopped(f'{len(survey.problems)} finding(s) above. Nothing was changed.')", "    if False:\n        raise ConversionStopped(f'{len(survey.problems)} finding(s) above. Nothing was changed.')", 'findings not stopping the run'),
    ("    if problems:\n        for problem in problems[:NAMES_SHOWN]:", "    if False:\n        for problem in problems[:NAMES_SHOWN]:", 'a faulty copy not stopping the run'),
    ("    if not rule.differ_in_line_endings_only(old, new) or sha256_of(new) != after:", "    if False:", 'converted bytes not checked against the list'),
    ("        elif path == SETTINGS_FILE:\n            data = full.read_bytes()", "        elif path == SETTINGS_FILE and False:\n            data = full.read_bytes()", 'the settings file not known'),
    ("        if look_only:\n            return _look(tree, entries, rule, say)", "        if False:\n            return _look(tree, entries, rule, say)", 'a look that goes on to convert'),
    ("    if wanted is None or found != wanted:", "    if False:", 'any rule file accepted'),
    ("            or record.get('conversion_list_sha256') != list_sha256):", "            or False):", 'a record of another list accepted'),
    ("        unknown = [path for path in list(survey.to_convert) + list(survey.to_remove)", "        unknown = [path for path in []", 'new files on a second run not noticed'),
    ("            if not os.listdir(current) and Path(current) != tree / 'records':\n                os.rmdir(current)", "            pass", 'empty folders left behind'),
    ("        originals.update({path: now_sha for path, (now_sha, then_sha) in survey.settings.items()\n                          if now_sha != then_sha})", "", 'the settings file not required in the copy'),
]
original = file.read_text(encoding='utf-8'); caught = 0
for old, new, what in MUTATIONS:
    if original.count(old) != 1:
        print('NOT APPLIED -', what, original.count(old)); continue
    file.write_text(original.replace(old, new), encoding='utf-8', newline='\n')
    try:
        run = subprocess.run([python, '-B', '-m', 'unittest', 'test_convert_to_file_form'], cwd=folder, capture_output=True, text=True)
    finally:
        file.write_text(original, encoding='utf-8', newline='\n')
    failed = run.returncode != 0; caught += failed
    print('CAUGHT' if failed else 'MISSED', '-', what)
print(caught, 'of', len(MUTATIONS), 'planted faults caught')
