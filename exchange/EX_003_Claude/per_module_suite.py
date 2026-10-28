"""NAMES-1 v0.2 design evidence: run each current test module separately and report tests, skips, result.
Usage: python3 -I per_module_suite.py TREE MOD [MOD ...]   (runs with -B, so the tree gets no bytecode)"""
import os, re, subprocess, sys, platform
tree, mods = sys.argv[1], sys.argv[2:]
env = {k: v for k, v in os.environ.items() if k != 'PYTHONPATH'}
env['PYTHONPATH'] = os.pathsep.join(os.path.join(tree, p) for p in ('src', os.path.join('src', 'methods'), 'tests'))
print('environment:', platform.system(), platform.release(), 'Python', platform.python_version())
total = 0
for m in mods:
    r = subprocess.run([sys.executable, '-B', '-m', 'unittest', '-v', m], cwd=tree, env=env, capture_output=True, text=True)
    err = r.stderr
    ran = int(re.search(r'Ran (\d+) test', err).group(1))
    skips = re.findall(r'^(\S+) \(([^)]*)\).*\.\.\. skipped (.*)$', err, re.M)
    status = err.strip().splitlines()[-1]
    total += ran
    print(f'{m:<45} ran {ran:3d}  skipped {len(skips)}  {status}')
    for s in skips:
        print('    skip:', s[0], '-', s[2])
print('total ran', total)
