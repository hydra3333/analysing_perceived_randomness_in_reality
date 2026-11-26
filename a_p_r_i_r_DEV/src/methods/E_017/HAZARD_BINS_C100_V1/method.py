"""E_17 variant HAZARD_BINS_C100_V1: the variant's own entry file.

What this file is for
    It is the one file the research code calls for this variant. In build step 1 (the folder layout) it holds no
    calculation of its own: it passes the task to the family's shared core, E_017/core_v1.py, which holds
    the calculation of every E_17 variant and picks this variant's fixed settings by the task's variant ID.
    It refuses a task that is for any other variant, so this folder only ever answers for itself.

Which part of the specification it carries out
    doc/Predictive_Randomness_System_Specification_v0_6.md section 3.2 (one folder per variant, holding
    method.py and VARIANT.json) and section 17.3, phase 1 (layout only: no computation changes).

Which of the project's own modules it uses
    E_017.core_v1    compute() and verify() of the family (the file that was E_017/contract.py)

What uses it
    src/methods/_common/method_table.py imports it when it builds the runner's table of methods.
"""
from E_017 import core_v1

# The variant this folder is. It equals the folder's name and the "variant" line of VARIANT.json beside it.
VARIANT_ID = 'HAZARD_BINS_C100_V1'


def require_this_variant(task) -> None:
    """Refuse a task that is not for this folder's variant.

    task: the frozen MethodTask the runner built; its variant_id says which variant is wanted.
    Returns nothing. Raises ValueError, naming both variants, if the task is for another one.
    """
    if task.variant_id != VARIANT_ID:
        raise ValueError(f'this is the method file of E_17 variant {VARIANT_ID}; the task is for variant '
                         f'{task.variant_id!r}. The method table sent it to the wrong folder.')


def compute(task, view):
    """Compute this variant's forecast scores for one target draw, from earlier draws only.

    task: the frozen MethodTask (game, method, variant, target draw, observation view).
    view: the permitted view: the draws before the target, and nothing else.
    Returns the family core's MethodOutput unchanged, for example
        MethodOutput(barrels={'MAIN': BarrelOutput(ranking=ScoredRanking({1: 0.25, 2: -0.5, ...}))}),
    or MethodOutput(barrels={}) where the core reports that there is not enough history.
    """
    require_this_variant(task)
    return core_v1.compute(task, view)


def verify(task, view, forecast, diagnostic) -> None:
    """Check the assembled record against the family core's second, differently written calculation.

    task, view: as for compute().  forecast: the assembled forecast record (a dict).  diagnostic: the diagnostic
    record, or None. Returns nothing; raises ValueError (from the core) if the record differs.
    """
    require_this_variant(task)
    core_v1.verify(task, view, forecast, diagnostic)
