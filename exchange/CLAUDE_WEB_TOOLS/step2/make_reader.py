"""Build step 2: writes src/research/reader.py, copying the view code from the old reader without change.

What this file is for
    The new engine's reader must build exactly the view the old reader builds. So the view class and the prefix
    parser are not retyped: this script takes their source text from src/methods/_common/game_draws_reader.py,
    character for character, and places it between the new module's header and its new functions (the template
    beside this file). A test in the package compares the two modules' definitions as parsed code.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 6; build plan v0.1 section 3 item 1.

Which of the project's own modules it uses
    None; it reads the old reader as text.

What uses it
    Claude, in the cloud workspace. Usage:  python make_reader.py <repository root>
"""
import ast
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OLD_READER = 'src/methods/_common/game_draws_reader.py'
TEMPLATE = HERE / 'reader_template.py'
OUTPUT = HERE / 'overlay' / 'src' / 'research' / 'reader.py'
# The old reader's top-level definitions that are copied, in the old file's order.
COPIED_NAMES = ('_DIGIT', 'VIEW_KINDS', '_REAL', '_ORDER_STATUS', '_E1_VARIANT', 'header_for', '_owned', 'DrawView',
                '_trusted_file_bytes', '_parse_prefix')
MARK = '# @@COPIED_FROM_THE_OLD_READER@@\n'


def main() -> int:
    """Write reader.py; print how many definitions were copied; return 0."""
    source = (Path(sys.argv[1]) / OLD_READER).read_text(encoding='utf-8')
    found = {}
    for node in ast.parse(source).body:
        names = [node.name] if isinstance(node, (ast.FunctionDef, ast.ClassDef)) else \
            [t.id for t in node.targets if isinstance(t, ast.Name)] if isinstance(node, ast.Assign) else []
        for name in names:
            if name in COPIED_NAMES:
                found[name] = ast.get_source_segment(source, node)
    assert set(found) == set(COPIED_NAMES), sorted(set(COPIED_NAMES) - set(found))
    constants = [found[name] + '\n' for name in COPIED_NAMES if name.isupper() or name.startswith('_') and name[1:].isupper()]
    definitions = ['\n\n' + found[name] + '\n' for name in COPIED_NAMES if not (name.isupper() or name.startswith('_') and name[1:].isupper())]
    copied = ''.join(constants + definitions) + '\n'
    template = TEMPLATE.read_text(encoding='utf-8')
    assert template.count(MARK) == 1
    OUTPUT.write_text(template.replace(MARK, copied), encoding='utf-8')
    print(f'reader.py written: {len(COPIED_NAMES)} definitions copied from {OLD_READER}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
