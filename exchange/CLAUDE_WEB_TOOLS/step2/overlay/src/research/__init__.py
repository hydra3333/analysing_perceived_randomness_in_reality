"""The research engine of the system ratified on 22 November 2026 (RAT-40).

What this file is for
    It makes this folder a Python package, so that its files are imported as research.<name>. The engine is new
    code beside the old system's (specification 17.3): nothing here imports the old runner, registry, dispatch
    or Mode H modules. It does one thing when the package is first imported: it sets the numerical libraries to
    one thread, before NumPy is loaded, so that a forecast never depends on how many threads a library would
    otherwise choose or on which launcher started the job.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md sections 3 to 11 (build step 2 of section 17.4);
    section 5.4 (the same code, configuration, seed and earlier draws in the same environment give the same
    content digest).

Which of the project's own modules it uses
    None.

What uses it
    Python, whenever a file of the engine is imported.
"""
import os

# The settings that fix NumPy's libraries to one thread; the old system's launchers set the same four.
THREAD_SETTINGS = ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS')
ONE_THREAD = '1'

for _name in THREAD_SETTINGS:
    os.environ[_name] = ONE_THREAD
