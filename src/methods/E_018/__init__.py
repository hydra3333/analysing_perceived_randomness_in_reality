"""E_18 - Mixtures of Recurrence Modes: the family's folder.

What this file is for
    It makes this folder a Python package, so that the family's files can be imported as E_018.core_v1 and
    E_018.variants. It holds no code. Each variant has its own folder here (method.py and
    VARIANT.json); the calculation they share is core_v1.py, their fixed settings are in variants.py, and the shared
    helper they use is _shared/recurrence_gaps_v1.py. Nothing in this folder reads a file, starts a process or touches
    orchestration.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 3.2. The method itself:
    doc/Predictive_Randomness_Wave2_E2_E17_E18_E19_Design_v0_1r2.md.

Which of the project's own modules it uses
    None.

What uses it
    Python, whenever a file of this family is imported.
"""
