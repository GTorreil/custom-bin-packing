"""
Tests for the custom bin packing algorithm.
"""

from time import perf_counter

from .custom_bin_packing import BinConstraint, CustomBinPackingSolverNaiveAndSlow


def tests_without_constraints() -> None:
    """
    Test solving without constraints.
    """
    assert CustomBinPackingSolverNaiveAndSlow(
        60, ["none", "none", "none", "none"]
    ).solve() == [15, 15, 15, 15]
    assert CustomBinPackingSolverNaiveAndSlow(
        61, ["none", "none", "none", "none"]
    ).solve() == [16, 15, 15, 15]


def test_with_impact_less_constraints() -> None:
    """
    Verify with constraints that do not impact the result.
    """
    assert CustomBinPackingSolverNaiveAndSlow(
        60, ["none", ("min", 5), "none", "none"]
    ).solve() == [15, 15, 15, 15]
    assert CustomBinPackingSolverNaiveAndSlow(
        61, ["none", ("min", 5), "none", "none"]
    ).solve() == [16, 15, 15, 15]


def test_with_impacting_constraints() -> None:
    """
    Test with constraints that impact the result.
    """
    assert CustomBinPackingSolverNaiveAndSlow(
        60, ["none", ("min", 30), ("max", 0), "none"]
    ).solve() == [
        15,
        30,
        0,
        15,
    ]


def test_performance() -> None:
    """
    Measure the performance of the algorithm.
    """
    # Create 1500 bins with varied constraints.
    bin_constraints: list[BinConstraint] = ["none", ("min", 30), ("max", 0)] * 500

    # Create a problem with a large number of bins and items.
    solver = CustomBinPackingSolverNaiveAndSlow(100000, bin_constraints)

    # Solve the problem
    start = perf_counter()
    solver.solve()
    end = perf_counter()

    target_time = 0.5  # TODO: adjust the target resolution time
    assert end - start < target_time, f"Resolution time: {end - start}s"
