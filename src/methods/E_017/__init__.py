"""E_17 - Discrete Recurrence Hazard Curves (revision 1; wave 2).

Specification: doc/Predictive_Randomness_Wave2_E2_E17_E18_E19_Design_v0_1r2.md. `variants` holds the fixed variant table and `contract` connects the method to
the shared contract runner. The gaps, exposures, bins and log-age sign are in the shared, reviewed helper
_common/recurrence_gaps.py (revision 1), which E_2, E_17, E_18 and E_19 all use. Nothing here reads a file,
starts a process or touches orchestration.
"""
