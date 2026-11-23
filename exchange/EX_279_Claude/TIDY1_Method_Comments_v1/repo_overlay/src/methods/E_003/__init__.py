"""E_3 - Occurrence-Curve Endpoint Forecast: the family's folder.

What this file is for
    It makes this folder a Python package, so that the family's files can be imported as E_003.core_v1 and
    E_003.variants. It holds no code. Each variant has its own folder here (method.py and
    VARIANT.json); the calculation they share is core_v1.py, their fixed settings are in variants.py, and the shared
    helper they use is _shared/polynomial_fits_v1.py. Nothing in this folder reads a file, starts a process or touches
    orchestration.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 3.2. The method itself:
    doc/Predictive_Randomness_E3_E4_Polynomial_Fit_Design_v0_1.md.

Which of the project's own modules it uses
    None.

What uses it
    Python, whenever a file of this family is imported.
"""
