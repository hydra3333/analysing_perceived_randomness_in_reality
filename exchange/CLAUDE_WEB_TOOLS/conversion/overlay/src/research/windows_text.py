"""The line ending the research engine writes in its text files: the Windows form, CRLF.

What this file is for
    The project's standard gives every text file a program writes the Windows form: each line ends CRLF. The
    engine builds its texts with a plain line feed between lines, as Python code does, and turns them into the
    standard's form in one place, here, just before the bytes are written. Nothing is left to the platform's
    default, so the engine writes the same bytes on the owner's PC and in the cloud. The line-record files
    (.jsonl) are the standard's one exception and never pass through this file: a list line is the canonical
    encoding, which ends in one line feed that is part of what is hashed.

Which part of the project's rules it carries out
    doc/FILE_FORM_STANDARD_v0_2.md (RAT-49) sections 1, 3 and 4.

Which of the project's own modules it uses
    None.

What uses it
    research/reports.py (report files, read-me files, the side file of making times), research/status_file.py
    (VARIANT_STATUS.ini), research/derived_check.py (the not-current marker) and research/job_lock.py (lock
    files).
"""
from __future__ import annotations

# The line ending of every text file the engine writes, and the value to give open(..., newline=) so that each
# '\n' the code writes becomes exactly this.
LINE_ENDING = '\r\n'


def windows_lines(text: str) -> str:
    """Text built with a line feed between lines, in the form the standard gives a text file.

    text    what the code built, each line ending '\\n', for example 'file,made\\nREADME.txt,2026-12-01 20:10\\n'
    Returns the same text with every line ending CRLF: 'file,made\\r\\nREADME.txt,2026-12-01 20:10\\r\\n'. A last
    line with no line ending keeps none.
    Refuses (ValueError) text that already holds a carriage return: it has been through here once, or it is not
    text the engine built, and changing it again would write a wrong file.
    """
    if '\r' in text:
        raise ValueError('the text already holds a carriage return; it must be built with line feeds only and '
                         'pass through windows_lines exactly once')
    return text.replace('\n', LINE_ENDING)
