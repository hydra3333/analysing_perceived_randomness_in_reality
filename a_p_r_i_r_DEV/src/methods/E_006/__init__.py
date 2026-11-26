"""E_6 - Per-Number Fitted Distribution Models: the family's folder.

What this file is for
    It makes this folder a Python package, so that the family's files can be imported as E_006.core_v1 and
    E_006.beta_bernoulli. It holds no code. Each variant has its own folder here (method.py and VARIANT.json);
    the calculation they share is core_v1.py, and the mathematics and the variants' settings are in
    beta_bernoulli.py. Nothing in this folder reads a file, starts a process or touches orchestration.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 3.2. The method itself:
    doc/Predictive_Randomness_E6_Specification_and_Method_Template_Design_v0_1.md section 2.

Which of the project's own modules it uses
    None.

What uses it
    Python, whenever a file of this family is imported.
"""
