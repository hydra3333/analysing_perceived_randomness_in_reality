"""Workspace check: plant one fault at a time in the engine's writers and see that the new tests catch it."""
import subprocess, sys, pathlib
root = pathlib.Path(sys.argv[1]); python = sys.argv[2]
MUTATIONS = [
    ('src/research/reports.py', "        data = windows_lines(text).encode('ascii')\n        path = self.root / name\n", "        data = text.encode('ascii')\n        path = self.root / name\n", 'a report written with LF'),
    ('src/research/reports.py', "'a', encoding='ascii', newline=LINE_ENDING)", "'a', encoding='ascii', newline='\\n')", 'the side file appended with LF'),
    ('src/research/reports.py', "        data = windows_lines(text).encode('ascii')\n        # Compared as bytes", "        data = text.encode('ascii')\n        # Compared as bytes", 'the side file tidied with LF'),
    ('src/research/reports.py', "        if path.read_bytes() != data:", "        if path.read_text(encoding='ascii') != text:", 'the side file compared as text, not bytes'),
    ('src/research/status_file.py', "    body = windows_lines('\\n'.join(lines) + '\\n').encode('ascii')", "    body = ('\\n'.join(lines) + '\\n').encode('ascii')", 'a status file body with LF'),
    ('src/research/status_file.py', "CHECK_LINE = b'[check]\\r\\n'", "CHECK_LINE = b'[check]\\n'", 'the check line with LF'),
    ('src/research/status_file.py', ".encode('ascii') + LINE_END\n\n\ndef read_status", ".encode('ascii') + b'\\n'\n\n\ndef read_status", 'the last line of a status file with LF'),
    ('src/research/derived_check.py', "newline=LINE_ENDING) as stream:", "newline='\\n') as stream:", 'the not-current marker with LF'),
    ('src/research/job_lock.py', "                 windows_lines(f'{self.purpose}; started {self.when}; process {os.getpid()}\\n').encode('ascii'))", "                 f'{self.purpose}; started {self.when}; process {os.getpid()}\\n'.encode('ascii'))", 'a lock file with LF'),
    ('src/research/windows_text.py', "    if '\\r' in text:", "    if False:", 'a second conversion not refused'),
    ('src/research/variant_lists.py', "        stream.write(line)", "        stream.write(line.replace(b'\\n', b'\\r\\n'))", 'a list header written CRLF'),
]
caught = 0
for path, old, new, what in MUTATIONS:
    file = root / path; original = file.read_text(encoding='utf-8')
    if original.count(old) != 1:
        print('NOT APPLIED', what, original.count(old)); continue
    file.write_text(original.replace(old, new), encoding='utf-8', newline='\n')
    try:
        run = subprocess.run([python, '-B', '-m', 'unittest', 'test_research_file_form'], cwd=root, capture_output=True, text=True,
                             env={'PYTHONPATH': 'src:src/methods:tests', 'PATH': '/usr/bin:/bin'})
    finally:
        file.write_text(original, encoding='utf-8', newline='\n')
    failed = run.returncode != 0
    caught += failed
    print('CAUGHT' if failed else 'MISSED', '-', what)
print(caught, 'of', len(MUTATIONS), 'planted faults caught')
