"""Synthetic regression test for DOC-10's CHECK_RESULTS_EOL.py (Claude, 1 Nov 2026; EX_119 C03).

Builds throwaway Git repositories in a temporary folder with INVENTED files under results/ (never a project record), commits
them with the DOC-10 rule `results/** -text`, then rewrites one file's working bytes per case and runs the checker.
Usage: python3 -I test_check_results_eol.py PATH_TO_CHECK_RESULTS_EOL.py
"""
import os, subprocess, sys, tempfile

CHK = os.path.abspath(sys.argv[1])
BASE = {'results/empty.log': b'', 'results/a/record.json': b'{"x": 1}\n', 'results/b/table.csv': b'h1,h2\n1,2\n'}
CASES = [   # (name, file to rewrite, new bytes or None to delete, expected result)
    ('all files as committed (one zero-byte file, two LF files)', None, None, 'PASS'),
    ('zero-byte file stays zero bytes', 'results/empty.log', b'', 'PASS'),
    ('nonempty file with no newline at all (w/none, size 6)', 'results/a/record.json', b'123456', 'STOP'),
    ('the empty log given content with no newline (w/none, size 3)', 'results/empty.log', b'abc', 'STOP'),
    ('CRLF rewrite of an LF record', 'results/b/table.csv', b'h1,h2\r\n1,2\r\n', 'STOP'),
    ('mixed endings', 'results/b/table.csv', b'h1,h2\r\n1,2\n', 'STOP'),
    ('a tracked record missing from the working tree', 'results/a/record.json', None, 'STOP'),
]


def git(repo, *a):
    return subprocess.run(['git', '-C', repo, *a], capture_output=True, text=True, check=True).stdout


def run_case(name, path, data, want):
    with tempfile.TemporaryDirectory() as td:
        git(td, 'init', '-q')
        git(td, 'config', 'user.email', 't@t'); git(td, 'config', 'user.name', 't')
        with open(os.path.join(td, '.gitattributes'), 'wb') as f:
            f.write(b'results/** -text\n')
        for p, b in BASE.items():
            os.makedirs(os.path.dirname(os.path.join(td, p)), exist_ok=True)
            with open(os.path.join(td, p), 'wb') as f:
                f.write(b)
        git(td, 'add', '-A'); git(td, 'commit', '-q', '-m', 'invented records')
        if path is not None:
            full = os.path.join(td, path)
            if data is None:
                os.remove(full)
            else:
                with open(full, 'wb') as f:
                    f.write(data)
        eol = git(td, 'ls-files', '--eol', '--', 'results').strip().replace('\t', '  ')
        r = subprocess.run([sys.executable, '-I', CHK, '--repo', td], capture_output=True, text=True)
        got = 'PASS' if (r.returncode == 0 and 'EOL PASS' in r.stdout) else ('STOP' if r.returncode == 1 and 'EOL STOP' in r.stdout else '??')
        ok = got == want
        print(f"{'ok  ' if ok else 'FAIL'} {name}: expected {want}, got {got} (exit {r.returncode})")
        for ln in eol.splitlines():
            print('       ls-files: ' + ln)
        for ln in r.stdout.strip().splitlines():
            print('       checker:  ' + ln)
        return ok


print('python', sys.version.split()[0], '| checker', CHK)
results = [run_case(*c) for c in CASES]
print(f'{sum(results)} of {len(results)} cases as expected')
sys.exit(0 if all(results) else 1)
