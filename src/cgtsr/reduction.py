"""
Deterministic greedy coverage-preserving test-suite reduction.

This module is a reference reproduction implementation reconstructed
from the frozen experimental protocol and empirical artifacts.

It is NOT represented as the original transient execution script that
produced the frozen CGTSR results.

Coverage criteria
-----------------
statement
    Executed production-source statement elements.

branch
    Executed coverage.py control-flow arc elements.

combined
    Union of statement and branch elements with explicit namespaces
    so that statement and branch representations cannot collide.

Selection rule
--------------
At each iteration:

1. Compute each unselected test's marginal gain with respect to the
   currently uncovered coverage universe.
2. Select the test with maximum marginal gain.
3. Resolve equal-gain ties deterministically by lexicographically
   smallest pytest test ID.
4. Continue until the complete observed coverage universe is covered.

This is a greedy coverage-preserving reduction. It does not claim
global minimum cardinality.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping


VALID_CRITERIA = {
    "statement",
    "branch",
    "combined",
}


@dataclass(frozen=True)
class ReductionResult:
    """Result of deterministic greedy coverage-preserving reduction."""

    criterion: str
    original_tests: int
    selected_tests: tuple[str, ...]
    coverage_elements: int
    coverage_preserved: bool

    @property
    def selected_count(self) -> int:
        return len(self.selected_tests)

    @property
    def removed_tests(self) -> int:
        return self.original_tests - self.selected_count

    @property
    def reduction_percent(self) -> float:
        if self.original_tests == 0:
            return 0.0

        return (
            100.0
            * self.removed_tests
            / self.original_tests
        )


def _as_element_set(value: Any) -> set[str]:
    """
    Convert a stored coverage-element representation to a string set.

    Frozen per-test artifacts represent statement and branch elements
    as collections of strings.
    """

    if value is None:
        return set()

    if isinstance(value, str):
        return {value}

    return {str(x) for x in value}


def statement_elements(
    record: Mapping[str, Any],
) -> set[tuple[str, str]]:
    """Return namespaced statement elements."""

    values = (
        record.get("statement_elements")
        or record.get("statements")
        or []
    )

    return {
        ("S", x)
        for x in _as_element_set(values)
    }


def branch_elements(
    record: Mapping[str, Any],
) -> set[tuple[str, str]]:
    """Return namespaced branch/arc elements."""

    values = (
        record.get("branch_arc_elements")
        or record.get("branch_elements")
        or record.get("arcs")
        or []
    )

    return {
        ("B", x)
        for x in _as_element_set(values)
    }


def coverage_elements(
    record: Mapping[str, Any],
    criterion: str,
) -> set[tuple[str, str]]:
    """
    Extract the requested coverage representation from one test record.
    """

    if criterion not in VALID_CRITERIA:
        raise ValueError(
            f"Unknown criterion {criterion!r}; "
            f"expected one of {sorted(VALID_CRITERIA)}"
        )

    if criterion == "statement":
        return statement_elements(record)

    if criterion == "branch":
        return branch_elements(record)

    return (
        statement_elements(record)
        | branch_elements(record)
    )


def coverage_universe(
    records: Mapping[str, Mapping[str, Any]],
    criterion: str,
) -> set[tuple[str, str]]:
    """Return the complete observed coverage universe."""

    universe: set[tuple[str, str]] = set()

    for record in records.values():
        universe.update(
            coverage_elements(
                record,
                criterion,
            )
        )

    return universe


def selected_coverage(
    records: Mapping[str, Mapping[str, Any]],
    selected_tests: Iterable[str],
    criterion: str,
) -> set[tuple[str, str]]:
    """Return coverage achieved by a supplied selected-test sequence."""

    covered: set[tuple[str, str]] = set()

    for test_id in selected_tests:

        if test_id not in records:
            raise KeyError(
                f"Selected test not found in records: {test_id}"
            )

        covered.update(
            coverage_elements(
                records[test_id],
                criterion,
            )
        )

    return covered


def greedy_reduce(
    records: Mapping[str, Mapping[str, Any]],
    criterion: str = "combined",
) -> ReductionResult:
    """
    Perform deterministic greedy coverage-preserving reduction.

    Parameters
    ----------
    records
        Mapping from pytest test ID to its frozen per-test coverage
        record.

    criterion
        ``statement``, ``branch``, or ``combined``.

    Returns
    -------
    ReductionResult
        Deterministically selected test IDs and preservation metadata.
    """

    if criterion not in VALID_CRITERIA:
        raise ValueError(
            f"Unknown criterion {criterion!r}"
        )

    # Precompute coverage sets once.
    test_elements = {
        test_id: coverage_elements(
            record,
            criterion,
        )
        for test_id, record in records.items()
    }

    universe: set[tuple[str, str]] = set()

    for elements in test_elements.values():
        universe.update(elements)

    uncovered = set(universe)
    selected: list[str] = []

    # Tests with empty coverage remain in the denominator but can
    # never contribute positive marginal gain.
    remaining = set(test_elements)

    while uncovered:

        best_test = None
        best_gain = 0

        # Sorting makes the tie rule explicit and reproducible.
        for test_id in sorted(remaining):

            gain = len(
                test_elements[test_id]
                & uncovered
            )

            if gain > best_gain:
                best_gain = gain
                best_test = test_id

        if best_test is None or best_gain <= 0:
            raise RuntimeError(
                "Coverage universe cannot be completed from "
                "the available per-test coverage records."
            )

        selected.append(best_test)

        uncovered.difference_update(
            test_elements[best_test]
        )

        remaining.remove(best_test)

    reproduced = selected_coverage(
        records,
        selected,
        criterion,
    )

    preserved = reproduced == universe

    return ReductionResult(
        criterion=criterion,
        original_tests=len(records),
        selected_tests=tuple(selected),
        coverage_elements=len(universe),
        coverage_preserved=preserved,
    )


def normalize_missing_tests(
    records: Mapping[str, Mapping[str, Any]],
    collected_test_ids: Iterable[str],
) -> dict[str, Mapping[str, Any]]:
    """
    Add collected tests absent from the per-test coverage mapping as
    explicit empty-coverage records.

    This reproduces the denominator-normalization rule used for
    attrs 24.1.0:

        Missing collected tests are represented as explicit empty
        coverage sets.

    Existing records are not modified.
    """

    normalized = dict(records)

    for test_id in collected_test_ids:

        if test_id not in normalized:
            normalized[test_id] = {
                "statement_elements": [],
                "branch_arc_elements": [],
            }

    return normalized
