"""Build step 2, proof tool: scan the package's Python files for the mechanical parts of the coding practices.

Usage: scan_practices.py <overlay folder>
For every .py file under the overlay it checks: a header; in the engine's own files the header's four parts; a
comment (docstring) on every function and class (test functions are named for their rule instead); only ASCII;
no unused import. The files copied byte for byte from passed work are listed and excused by name. It prints one
line a finding and ends with RESULT: PASS or RESULT: FAIL. It reads only.
"""
import ast
import sys
from pathlib import Path

# The four parts every engine file's header holds (doc/CODING_PRACTICES_v0_1.md section 1).
HEADER_PARTS = ('What this file is for', 'Which part of the specification', "Which of the project's own modules",
                'What uses it')
# Files whose bytes are passed work, kept as they are: the kernel and its tests; the reader's copied definitions.
EXCUSED = {'src/research/ov1_numeric.py': 'the passed kernel, byte for byte',
           'tests/test_research_ov1_numeric.py': 'the passed kernel\'s tests (one import line changed)',
           'src/research/reader.py': 'holds the old reader\'s definitions, copied character for character'}


def findings_of(path: Path, name: str) -> list:
    """The findings for one file, as text lines; [] if it is clean."""
    text = path.read_text(encoding='utf-8')
    tree, found = ast.parse(text), []
    header = ast.get_docstring(tree)
    if not header:
        found.append('no header')
    elif name.startswith('src/') and name not in EXCUSED:
        found += [f'the header lacks "{part}"' for part in HEADER_PARTS if part not in header]
    if not text.isascii():
        found.append('not ASCII')
    if name not in EXCUSED:
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and not ast.get_docstring(node) \
                    and not (name.startswith('tests/') and node.name.startswith('test_')):
                found.append(f'no comment on {node.name} (line {node.lineno})')
    imported = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update({(a.asname or a.name).split('.')[0]: node.lineno for a in node.names})
        elif isinstance(node, ast.ImportFrom):
            imported.update({a.asname or a.name: node.lineno for a in node.names})
    used = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
    found += [f'unused import {word} (line {line})' for word, line in sorted(imported.items())
              if word not in used and word != 'annotations']
    return found


def main(overlay: Path) -> int:
    """Scan every Python file of the overlay; print the findings; return 0 only if there is none."""
    files = sorted(overlay.rglob('*.py'))
    total = 0
    for path in files:
        name = path.relative_to(overlay).as_posix()
        for finding in findings_of(path, name):
            total += 1
            print(f'{name}: {finding}')
    for name, why in sorted(EXCUSED.items()):
        print(f'excused from the header and comment checks: {name} ({why})')
    print(f'{len(files)} Python files scanned; {total} findings')
    print('RESULT: PASS' if total == 0 else 'RESULT: FAIL')
    return 0 if total == 0 else 1


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1]).resolve()))
