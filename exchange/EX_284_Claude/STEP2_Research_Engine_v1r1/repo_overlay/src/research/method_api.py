"""The one exception a method raises when its own mathematics cannot produce a forecast.

What this file is for
    A method's compute() raises MethodFailed when its own calculation cannot be made for a target (for example a
    fit that has no solution). The research engine then records NO_FORECAST with the reason METHOD_FAILED, which
    is final for that target. Any other exception is treated as a fault of the environment or of the code: no
    line is written and the job stops for that game.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 5.3 ("the one declared exception type").

Which of the project's own modules it uses
    None.

What uses it
    research/forecast_engine.py catches it; a variant's method.py or a helper may raise it.
"""


class MethodFailed(Exception):
    """Raised by a method for a failure of its own mathematics at one target.

    The message says what could not be computed, for example
        MethodFailed('E_3 POLY_LS_W52_D2_V1: the normal equations are singular for barrel MAIN').
    """
