"""The research engine of the system ratified on 22 November 2026 (RAT-40).

What this file is for
    It makes this folder a Python package, so that its files are imported as research.<name>. It holds no code.
    The engine is new code beside the old system's (specification 17.3): nothing here imports the old runner,
    registry, dispatch or Mode H modules.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md sections 3 to 11 (build step 2 of section 17.4).

Which of the project's own modules it uses
    None.

What uses it
    Python, whenever a file of the engine is imported.
"""
