"""The light tidy-up of the existing method files: the builder that adds the headers and comments.

What this file is for
    It makes the whole tidy-up mechanically, in a disposable copy of the project: each existing method file gets
    a header in the form of the coding practices, the functions that had no comment get one, and the constants
    of each family core get a note. It then proves, file by file, that nothing but comments changed: the code
    of each file, with every comment and docstring taken out, must be identical before and after. It refuses
    (an assertion) on anything unexpected, and it never runs against the owner's checkout.

Which part of the specification it carries out
    The owner's note of ratification RAT-40, item 3 (decision log entry 147), and doc/CODING_PRACTICES_v0_1.md
    section 6: "each existing method file is given its header and dependency list, and comments where they are
    plainly missing. No calculation changes".

Which of the project's own modules it uses
    None. The texts it adds are in tidy_texts.py, and the comparison of code without comments is code_only in
    check_comments_only.py; both are beside this file.

What uses it
    Nothing in the project. It is kept as the record of how the tidy-up package was made.

Usage:  python make_tidy_up.py <a disposable Git clone of the project at the base commit>
"""
from __future__ import annotations

import ast
import re
import sys
import textwrap
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import tidy_texts as T   # noqa: E402  (the texts live beside this file)
from check_comments_only import code_only   # noqa: E402  (the proof that only comments changed)

# The three shared helpers, and the family folders that follow the common pattern (core_v1.py and variants.py).
SHARED_HELPERS = ('occurrence_counts_v1', 'polynomial_fits_v1', 'recurrence_gaps_v1')

# The files of E_1 that the tidy-up leaves alone, and why: the old system's archive tests rebuild E_1's earlier
# revisions from these files' bytes and compare two of them with reference hashes (tests/test_code3_retirement.py,
# tests/test_e1r3_revision3.py). A reference is never refreshed, so these files keep their bytes.
E1_FILES_LEFT_ALONE = ('E_001/__init__.py', 'E_001/e1_common_reader_bridge.py',
                       'E_001/e1_historical_appearance_frequency.py', 'E_001/e1_standalone_contract.py',
                       'E_001/e1_training_view.py', 'E_001/multigame_e1.py')

# Indentation of the header sections' bodies inside a module docstring.
KEPT_TEXT_INDENT = '    '

# The longest line the tidy-up writes; a longer line of new wording is wrapped. (Earlier wording that is kept
# word for word is never re-wrapped.)
LINE_LIMIT = 118

# Stand-ins for an earlier header while the new wording around it is wrapped.
KEPT_DOC_MARK, KEPT_BODY_MARK = '@@KEPT-DOC@@', '@@KEPT-BODY@@'


def module_docstring_span(source: str) -> tuple:
    """Where a file's module docstring is, and its text.

    source: the file's text.
    Returns (first line index, line index after its last line, the docstring's text), lines counted from 0, for
    example (0, 7, 'E_7 - Bayesian Frequency Shrinkage ...'). Refuses a file that does not begin with one.
    """
    tree = ast.parse(source)
    first = tree.body[0]
    assert isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant), 'no module docstring'
    return first.lineno - 1, first.end_lineno, first.value.value


def kept(text: str) -> str:
    """Indent an earlier header so that it can be kept, word for word, inside the new header."""
    return textwrap.indent(text.strip('\n'), KEPT_TEXT_INDENT)


def body_after_first_paragraph(old_doc: str) -> str:
    """An earlier header without its one-line title: the text from its second paragraph on."""
    parts = old_doc.strip('\n').split('\n\n', 1)
    return parts[1] if len(parts) == 2 else parts[0]


def wrapped(text: str) -> str:
    """Wrap every line of new wording that is longer than LINE_LIMIT, keeping the line's own indentation.

    text: the wording, for example a header or a function's comment.
    Returns the same wording with long lines folded; a folded line's continuation is indented like the line.
    """
    out = []
    for line in text.split('\n'):
        if len(line) <= LINE_LIMIT:
            out.append(line)
            continue
        indent = line[:len(line) - len(line.lstrip())]
        out += textwrap.wrap(line.strip(), LINE_LIMIT, initial_indent=indent, subsequent_indent=indent,
                             break_long_words=False, break_on_hyphens=False)
    return '\n'.join(out)


def module_lines(pairs: list) -> str:
    """The header's list of the project's modules a file uses, in two aligned columns.

    pairs: [(module, what it is used for), ...], for example [('_common.game_profiles', 'get_profile: ...')].
    Returns the indented lines, one for each module.
    """
    width = max(len(module) for module, _use in pairs) + 2
    hanging = ' ' * (len(KEPT_TEXT_INDENT) + width)
    return '\n'.join(textwrap.fill(use, LINE_LIMIT, initial_indent=f'{KEPT_TEXT_INDENT}{module:<{width}}',
                                   subsequent_indent=hanging, break_long_words=False, break_on_hyphens=False)
                     for module, use in pairs)


def new_header_for(relative: str, old_doc: str) -> str:
    """The new module header of one file.

    relative: the file's path from src/methods, for example 'E_007/core_v1.py'.  old_doc: its present header.
    Returns the header's text, without the quotation marks. Refuses a file the tidy-up has no header for.
    """
    fill = dict(layout=T.LAYOUT_SPEC, e6=T.E6_DESIGN, wave1=T.WAVE1, wave2=T.WAVE2, poly=T.POLY,
                old_doc=KEPT_DOC_MARK, old_body=KEPT_BODY_MARK)
    if relative in T.FULL_HEADERS:
        template = T.FULL_HEADERS[relative]
    else:
        family, name = relative.split('/')
        f = T.FAMILIES[family]
        fill.update(f, family=family, design_doc=f['design'].split(' section')[0], settings_module='variants',
                    helper_sentence=f', their fixed settings are in variants.py, and the shared helper they use is '
                                    f'_shared/{f["helper"]}.py. Nothing in this folder reads a file, starts a process '
                                    f'or touches orchestration.',
                    modules=module_lines([
                        (f'{family}.variants', "VARIANTS: each variant's fixed settings"),
                        (f'_shared.{f["helper"]}', T.HELPER_USE[f['helper']]),
                        ('_common.contract_forecast', f'the types a method returns ({f["outputs"]})'),
                        ('_common.game_profiles', "get_profile: each game's barrels (lowest and highest number, "
                                                  'how many are drawn)')]))
        template = {'core_v1.py': T.CORE_HEADER, 'variants.py': T.VARIANTS_HEADER, '__init__.py': T.INIT_HEADER}[name]
    header = wrapped(template.format(**fill))
    assert header.count(KEPT_DOC_MARK) + header.count(KEPT_BODY_MARK) <= 1, relative
    return (header.replace(KEPT_DOC_MARK, kept(old_doc))
            .replace(KEPT_BODY_MARK, kept(body_after_first_paragraph(old_doc))))


def uncommented_functions(source: str) -> list:
    """The names of a file's functions that have no docstring.

    source: the file's text.
    Returns for example ['_config', '_scores', 'compute']; nested functions and methods are named 'outer.inner'
    and 'Class.method'.
    """
    names = []

    def visit(node, prefix):
        """Walk one node's children, adding to `names`; prefix is the dotted name of the enclosing function or class."""
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if not isinstance(child, ast.ClassDef) and ast.get_docstring(child) is None:
                    names.append(prefix + child.name)
                visit(child, prefix + child.name + '.')
            else:
                visit(child, prefix)

    visit(ast.parse(source), '')
    return names


def function_docs_for(relative: str, source: str) -> dict:
    """The comments to add to one file's functions that have none.

    relative: the file's path from src/methods.  source: the file's text.
    Returns {function name: comment text}, for example {'_config': 'Check that the task ...'}: the text written
    out for that file in tidy_texts.FUNCTION_DOCS, or, for the functions every family core has in the same
    form, the shared text filled in with the family's own words.
    """
    docs = dict(T.FUNCTION_DOCS.get(relative, {}))
    family, name = relative.split('/')[0], relative.split('/')[-1]
    if name == 'core_v1.py' and family in T.FAMILIES:
        f = T.FAMILIES[family]
        polynomial = 'poly_pick' in f
        chances = (', both as its score and as its published chance' if f['chances'] else '')
        shared = {'_config': T.DOC_CONFIG.format(**f),
                  '_scores': T.DOC_SCORES.format(**f),
                  '_score': T.DOC_SCORE_POLY.format(**f) if polynomial else None,
                  'compute': T.DOC_COMPUTE_POLY.format() if polynomial else T.DOC_COMPUTE.format(chances=chances)}
        for function in uncommented_functions(source):
            if function not in docs and shared.get(function):
                docs[function] = shared[function]
    return docs


def add_function_docs(source: str, docs: dict, relative: str) -> str:
    """Give each named function, which must have no docstring yet, the comment written for it.

    source: the file's text.  docs: {function name: comment text}.  relative: the file's path, for messages.
    Returns the new text. Refuses if a named function is not found, already has a docstring, or if any function
    of the file would still be left without one.
    """
    tree = ast.parse(source)
    lines = source.split('\n')
    found, insertions = set(), []

    def visit(node, prefix):
        """Walk one node's children, noting in `insertions` where each comment goes; prefix is the enclosing name."""
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                name = prefix + child.name
                if isinstance(child, ast.ClassDef):
                    assert ast.get_docstring(child), f'{relative}: class {name} has no docstring'
                elif ast.get_docstring(child) is None:
                    assert name in docs, f'{relative}: function {name} has no docstring and none is written for it'
                    first = child.body[0]
                    indent = ' ' * first.col_offset
                    text = wrapped(docs[name].strip('\n'))
                    block = ([f'{indent}"""{text}"""'] if '\n' not in text else
                             [f'{indent}"""' + text.split('\n')[0]]
                             + [(indent + line) if line else '' for line in text.split('\n')[1:]] + [f'{indent}"""'])
                    insertions.append((first.lineno - 1, block))
                    found.add(name)
                else:
                    assert name not in docs, f'{relative}: function {name} already has a docstring'
                visit(child, name + '.')
            else:
                visit(child, prefix)

    visit(tree, '')
    assert found == set(docs), f'{relative}: not found: {sorted(set(docs) - found)}'
    for line_index, block in sorted(insertions, reverse=True):
        lines[line_index:line_index] = block
    return '\n'.join(lines)


def add_constant_notes(source: str) -> str:
    """Put one note above a family core's block of constants, saying what each of them is.

    source: the file's text.
    Returns the new text; unchanged if the file has no `METHOD_ID = ` line.
    """
    lines = source.split('\n')
    starts = [i for i, line in enumerate(lines) if line.startswith('METHOD_ID = ')]
    if not starts:
        return source
    assert len(starts) == 1
    present = [name for name in T.CONSTANT_NOTES if any(line.startswith(name + ' = ') for line in lines)]
    width = max(len(name) for name in present)
    note = ['# The fixed identity and output settings of this family; they never change:'] + \
           [f'#   {name:<{width}}  {T.CONSTANT_NOTES[name]}' for name in present]
    lines[starts[0]:starts[0]] = note
    return '\n'.join(lines)


def add_constant_comments(source: str, relative: str) -> str:
    """Put the comment written for it above each other constant of a file that had none.

    source: the file's text.  relative: the file's path from src/methods.
    Returns the new text. Refuses if a named constant is not found exactly once, or already has a comment.
    """
    lines = source.split('\n')
    for name, comment in T.CONSTANT_COMMENTS.get(relative, {}).items():
        at = [i for i, line in enumerate(lines) if line.startswith(name + ' = ')]
        assert len(at) == 1, f'{relative}: constant {name} found {len(at)} times'
        assert '#' not in lines[at[0]] and not lines[at[0] - 1].startswith('#'), f'{relative}: {name} has a comment'
        lines[at[0]:at[0]] = comment
    return '\n'.join(lines)


def tidy_one_file(path: Path, relative: str) -> None:
    """Tidy one file in place and prove that only comments changed.

    path: the file.  relative: its path from src/methods.
    Returns nothing. Refuses (an assertion) if the code differs afterwards, or the text is not plain ASCII.
    """
    before = path.read_text(encoding='utf-8')
    start, end, old_doc = module_docstring_span(before)
    lines = before.split('\n')
    header = new_header_for(relative, old_doc).strip('\n')
    lines[start:end] = ['"""' + header.split('\n')[0]] + header.split('\n')[1:] + ['"""']
    with_header = '\n'.join(lines)
    after = add_function_docs(with_header, function_docs_for(relative, with_header), relative)
    after = add_constant_comments(add_constant_notes(after), relative)
    assert code_only(after) == code_only(before), f'{relative}: the code changed'
    assert after.isascii() and '\r' not in after and after.endswith('\n'), relative
    assert not any(line != line.rstrip() for line in after.split('\n')), f'{relative}: trailing spaces'
    path.write_bytes(after.encode('ascii'))


def files_to_tidy(methods: Path) -> list:
    """The existing method files the tidy-up covers, as paths from src/methods, in order.

    methods: <tree>/src/methods.
    Returns for example ['E_001/FULL_HISTORY_RAW_COUNTS_V1/method.py', 'E_002/__init__.py', ...]: every family's
    own modules except E_1's pinned ones, E_1's variant file, and the shared helpers. The 39 method.py files
    written in build step 1 already have the headers of the coding practices and are not touched.
    """
    chosen = ['E_001/FULL_HISTORY_RAW_COUNTS_V1/method.py']
    for family in sorted(p.name for p in methods.iterdir() if re.fullmatch(r'E_\d{3}', p.name)):
        if family == 'E_001':
            continue
        chosen += sorted(f'{family}/{p.name}' for p in (methods / family).glob('*.py'))
    chosen += [f'_shared/{helper}.py' for helper in SHARED_HELPERS]
    return chosen


def main() -> int:
    """Tidy every covered file of the tree named on the command line; print what was done; return 0."""
    methods = Path(sys.argv[1]).resolve() / 'src' / 'methods'
    chosen = files_to_tidy(methods)
    for relative in E1_FILES_LEFT_ALONE:
        assert (methods / relative).is_file() and relative not in chosen
    for relative in chosen:
        tidy_one_file(methods / relative, relative)
    print(f'files tidied: {len(chosen)}; E_1 files left alone (pinned by the old archive tests): {len(E1_FILES_LEFT_ALONE)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
