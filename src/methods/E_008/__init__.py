"""E_8 - Hierarchical Dirichlet-Multinomial Propensity (revision 1; wave 1).

Specification: doc/Predictive_Randomness_Wave1_E7_E8_E9_E10_Design_v0_1r1.md. `variants` holds the fixed variant table and `contract` connects the method to
the shared contract runner. The counting is in the shared, reviewed helper _common/occurrence_counts.py
(revision 1), which E_7, E_8, E_9 and E_10 all use. Nothing here reads a file, starts a process or touches
orchestration.
"""
