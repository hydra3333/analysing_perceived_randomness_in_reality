"""Workspace helper (not project code): the planted faults for slice C part C1 (the checks that travel with the
installed software, Verify_Tree.bat, the `checks` command). One fault at a time is planted in a disposable copy of
the dev tree that holds the overlay; the part's two test modules must fail. A fault no test catches is printed as
SURVIVED. Run it with nothing else running: slice A's process rule lists a Python process that ends while it is read."""
import subprocess
from pathlib import Path
MUT = Path('/home/claude/work/mut'); PY = '/home/claude/work/venv315/bin/python'
MODULES = ['test_trees_checks', 'test_trees_verify']
T, V, P = 'src/research/tree_checks.py', 'src/research/tree_verify.py', 'src/tree_checks_command.py'
FAULTS = [
 (T, "if content['status'] == FORECAST and set(content['barrels']) == {b.barrel_id for b in profile.barrels}:", "if content['status'] == FORECAST:", 'smoke: a forecast that lacks a barrel passes'),
 (T, "found = f'{content[\"status\"]}, {content.get(\"reason\")}' + (f' ({detail})' if detail else '')", "found = None", 'smoke: an answer that is no forecast passes'),
 (T, "found = f'{type(fault).__name__}: {fault}'", "found = None", 'smoke: an error in the method passes'),
 (T, "        shutil.rmtree(folder)\r\n        return None", "        return None", 'smoke: a passed smoke case leaves its folder'),
 (T, "target = first_target(game_id, variant.minimum_earlier_draws(game_id))", "target = first_target(game_id, variant.minimum_earlier_draws(game_id)) + 5", 'smoke: more history than the declared minimum is given'),
 (T, "generator = random.Random(f'{SMOKE_SEED}:{game_id}:{draw}')", "generator = random.Random()", 'smoke: the invented table is not the same every time'),
 (T, "    if is_link(scratch) or (scratch.exists() and not scratch.is_dir()):", "    if False:", 'smoke: a scratch folder that is a link is written through'),
 (T, "        if only is not None and variant.identity not in only:", "        if False:", 'smoke: every variant is tried when some were named'),
 (T, "            if not variant.supports(game_id):", "            if False:", 'smoke: a variant is tried for a game it does not support'),
 (T, "    return [forecasts[0], forecasts[len(forecasts) // 2], forecasts[-1]]", "    return [forecasts[0]]", 'sample: only the first stored forecast is computed again'),
 (T, "sorted(target for target, facts in state.targets.items() if facts.status == FORECAST)", "sorted(target for target, facts in state.targets.items())", 'sample: lines without a forecast are in the sample'),
 (T, "same = content_digest(content) == state.targets[target].content_digest", "same = True", 'sample: a forecast that comes out otherwise is not seen'),
 (T, "same, why = False, f'it could not be computed again", "same, why = True, f'it could not be computed again", 'sample: a forecast that cannot be computed again is no difference'),
 (T, "known = cutoff is not None and cutoff[1] == derived_check.MISMATCH and cutoff[0] <= found[0]", "known = cutoff is not None", 'derived: any marker makes a difference known'),
 (T, "known = cutoff is not None and cutoff[1] == derived_check.MISMATCH and cutoff[0] <= found[0]", "known = cutoff is not None and cutoff[1] == derived_check.MISMATCH", 'derived: a difference before the marked draw is called known'),
 (T, "found = derived_check.first_mismatch(records, cutoff[0] if awaiting else None)", "found = derived_check.first_mismatch(records, None)", 'derived: draws awaiting a catch-up are compared'),
 (T, "        answers[game_id] = (found[0], found[1], known)", "        answers[game_id] = None", 'derived: a difference is reported as agreement'),
 (T, "            if pass_on:\r\n                raise\r\n", "", 'reading: read_stored swallows a refusal'),
 (T, "        except GAME_REFUSALS as refusal:\r\n            if pass_on:", "        except GAME_REFUSALS + (KeyError, ValueError, TypeError) as refusal:\r\n            if pass_on:", 'reading: a fault is taken for an understood refusal'),
 (T, "        if unknown:", "        if False:", 'checks: a smoke case for a variant that is not there is not refused'),
 (T, "        with open(chosen.result, 'x', encoding='ascii', newline='\\n') as stream:", "        with open(chosen.result, 'w', encoding='ascii', newline='\\n') as stream:", 'checks: an existing result file is overwritten'),
 (T, "        only = None if smoke == ALL_VARIANTS else list(smoke)", "        only = None", 'checks: every smoke case is made when some were named'),
 (T, "        if sample:\r\n", "        if True:\r\n", 'checks: the sample is made when it was not asked'),
 (T, "    return EXIT_RAN\r\n", "    return EXIT_REFUSED\r\n", 'checks: the exit code says refused when it ran'),
 (V, "        if settings.role not in INSTALLED_ROLES:", "        if False:", 'verify: DEV is verified'),
 (V, "        check_no_unfinished_operation(settings.tree_root)", "        pass", 'verify: an unfinished operation does not refuse'),
 (V, "        check_no_orphan_marker(settings.tree_root)", "        pass", 'verify: the orphan marker does not refuse'),
 (V, "        process_rule.check_no_other_process_of_tree(settings.tree_root)\r\n    except", "        pass\r\n    except", 'verify: no process check before the first backup'),
 (V, "    looked_at = process_rule.check_no_other_process_of_tree(settings.tree_root)", "    looked_at = 0", 'verify: no process check under the lock'),
 (V, "        with job_lock(settings.tree_root, 'verify tree', started):\r\n            exit_code, closing = verify_locked(settings, now, say)", "        if True:\r\n            exit_code, closing = verify_locked(settings, now, say)", 'verify: the job lock is not taken'),
 (V, "    check_software_is_as_installed(settings)", "    pass", 'verify: software that is not what was installed passes'),
 (V, "    if status_refusals:", "    if False:", 'verify: a status file that fails its check passes'),
 (V, "    mark_due(settings)", "    pass", 'verify: the note that a backup is owed is not written'),
 (V, "    if smoke_failures:", "    if False:", 'verify: a failed smoke case does not withhold the marker'),
 (V, "        marker.unlink(missing_ok=True)", "        pass", 'verify: an older marker is left after a failure'),
 (V, "    closing = [SUITE_LINE]", "    closing = []", 'verify: the summary does not say that the suite was not run'),
 (V, "    digest = write_marker(settings.venv_dir)", "    digest = 'not written'", 'verify: the marker is not written'),
 (V, "    say(attempt_snapshot(settings, 'PRE_VERIFY', now).line())", "    pass", 'verify: no backup is attempted before'),
 (V, "    say(attempt_snapshot(settings, 'POST_VERIFY', now).line())", "    pass", 'verify: no backup is attempted after'),
 (V, "    log_verification(settings, 'VERIFIED', digest, summary, now)", "    pass", 'verify: no log line for a verification'),
 (V, "        log_verification(settings, 'NOT_VERIFIED', None, summary, now)", "        pass", 'verify: no log line for a failed verification'),
 (V, "    if differences:", "    if False:", 'verify: the sample\'s differences are not in the summary'),
 (V, "    for game_id in changed:", "    for game_id in ():", 'verify: a derived difference is not in the summary'),
 (V, "    for game_id, why in sorted(unreadable.items()):", "    for game_id, why in ():", 'verify: an unreadable game is not in the summary'),
 (P, "    if os.path.normcase(os.path.realpath(running)) != os.path.normcase(os.path.realpath(environment_folder)):", "    if False:", 'program: a Python that is not the tree\'s own is accepted'),
 (P, "    if arguments[0] == 'checks':", "    if False:", 'program: checks is held to the Python of the folder it lies in'),
 (P, "    if arguments[0] == 'verify':\r\n        from research.tree_verify import main", "    if arguments[0] != 'verify':\r\n        from research.tree_verify import main", 'program: the two commands are exchanged'),
]
survived = 0
for relative, old, new, what in FAULTS:
    path = MUT / relative; kept = path.read_bytes()
    assert kept.count(old.encode()) == 1, (what, kept.count(old.encode()))
    path.write_bytes(kept.replace(old.encode(), new.encode()))
    try:
        run = subprocess.run([PY, '-B', '-m', 'unittest', *(MODULES if relative == T else MODULES[1:])], cwd=MUT, timeout=300,
                             env={'PYTHONPATH': 'src:src/methods:tests', 'PATH': '/usr/bin:/bin'}, capture_output=True, text=True)
        caught, how = run.returncode != 0, 'caught  '
    except subprocess.TimeoutExpired:
        caught, how = True, 'caught (the tests did not end)'
    path.write_bytes(kept)
    survived += not caught
    print((how if caught else 'SURVIVED'), '|', what, flush=True)
print(f'{len(FAULTS)} faults planted; {survived} survived')
