"""E_4 - Occurrence-Curve Gradient Forecast (revision 1: exact polynomial fits, including Chebyshev minimax).

Specification: doc/Predictive_Randomness_E3_E4_Polynomial_Fit_Design_v0_1.md. This folder is self-contained:
`variants` holds the fixed variant table, `contract` connects the method to the shared contract runner. The
fits themselves are in the shared, reviewed helper _common/polynomial_fits.py (revision 1), which E_3 and E_4
both use. Neither module here reads a file, starts a process or touches orchestration.
"""
