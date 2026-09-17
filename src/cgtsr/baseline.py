"""
Size-matched random baseline for CGTSR.

REFERENCE REPRODUCTION IMPLEMENTATION
-------------------------------------

This module reconstructs the frozen random-baseline procedure from
the archived protocol and trial artifacts.

It is not represented as the original transient execution script.

Frozen procedure
----------------
For each release:

1. Use the combined statement + branch coverage representation.
2. Let k equal the number of tests selected by combined CGTSR.
3. Sort all pytest test IDs lexicographically.
4. Initialize one ``random.Random(release_seed)`` instance.
5. Draw 1,000 subsets of size k using ``rng.sample`` without
   replacement.
6. Keep the same RNG instance across all trials for that release.
7. Measure the fraction of the complete combined coverage universe
   retained by each sampled subset.

The release seeds are assigned sequentially from the frozen base seed
20260915 in the frozen 12-release order.

The empirical baseline compares coverage retention at equal suite
size. It is not a proof of global optimality and is not a test of
fault-detection equivalence.
"""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Any, Mapping, Sequence

from .reduction import (
    coverage_elements,
    coverage_universe,
)


DEFAULT_REPETITIONS = 1000
BASE_SEED = 20260915


@dataclass(frozen=True)
class RandomTrial:
    """One size-matched random-baseline trial."""

    trial: int
    seed: int
    original_tests: int
    sample_size: int
    universe_elements: int
    covered_elements: int
    retention_percent: float


def combined_test_sets(
    records: Mapping[str, Mapping[str, Any]],
) -> dict[str, set[tuple[str, str]]]:
    """
    Precompute combined statement-and-branch coverage for every test.
    """

    return {
        test_id: coverage_elements(
            record,
            "combined",
        )
        for test_id, record in records.items()
    }


def combined_universe(
    records: Mapping[str, Mapping[str, Any]],
) -> set[tuple[str, str]]:
    """Return the complete combined frozen coverage universe."""

    return coverage_universe(
        records,
        "combined",
    )


def covered_elements_for_sample(
    test_sets: Mapping[
        str,
        set[tuple[str, str]],
    ],
    sample: Sequence[str],
) -> set[tuple[str, str]]:
    """Return combined coverage achieved by one sampled test subset."""

    covered: set[tuple[str, str]] = set()

    for test_id in sample:

        if test_id not in test_sets:
            raise KeyError(
                f"Unknown test ID in random sample: {test_id}"
            )

        covered.update(
            test_sets[test_id]
        )

    return covered


def run_size_matched_random_baseline(
    records: Mapping[str, Mapping[str, Any]],
    sample_size: int,
    release_seed: int,
    repetitions: int = DEFAULT_REPETITIONS,
) -> list[RandomTrial]:
    """
    Reproduce the frozen size-matched random-baseline procedure.

    Parameters
    ----------
    records
        Frozen per-test coverage mapping.

    sample_size
        Number of tests in every random subset. For the study this
        equals the corresponding combined CGTSR selected-suite size.

    release_seed
        Frozen release-specific random seed.

    repetitions
        Number of random subsets. The frozen study used 1,000.

    Returns
    -------
    list[RandomTrial]
        Trial-level combined coverage-retention results.
    """

    if repetitions < 1:
        raise ValueError(
            "repetitions must be >= 1"
        )

    population = sorted(
        records.keys()
    )

    n = len(population)

    if sample_size < 0:
        raise ValueError(
            "sample_size must be >= 0"
        )

    if sample_size > n:
        raise ValueError(
            f"sample_size={sample_size} exceeds "
            f"population size={n}"
        )

    test_sets = combined_test_sets(
        records
    )

    universe = combined_universe(
        records
    )

    universe_size = len(universe)

    rng = random.Random(
        release_seed
    )

    trials: list[RandomTrial] = []

    for trial_number in range(
        1,
        repetitions + 1,
    ):

        sample = rng.sample(
            population,
            sample_size,
        )

        covered = covered_elements_for_sample(
            test_sets,
            sample,
        )

        covered_count = len(covered)

        if universe_size == 0:
            retention = 100.0
        else:
            retention = (
                100.0
                * covered_count
                / universe_size
            )

        trials.append(
            RandomTrial(
                trial=trial_number,
                seed=release_seed,
                original_tests=n,
                sample_size=sample_size,
                universe_elements=universe_size,
                covered_elements=covered_count,
                retention_percent=retention,
            )
        )

    return trials
