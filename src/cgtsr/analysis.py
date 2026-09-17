"""
Statistical analysis utilities for the CGTSR replication package.

REFERENCE REPRODUCTION IMPLEMENTATION
-------------------------------------

This module reconstructs the analysis applied to the frozen empirical
artifacts. It does not rerun subject test suites or runtime benchmarks.

The frozen runtime protocol used one warm-up followed by five measured
repetitions for each full and reduced suite, alternating execution
order with coverage instrumentation disabled.

The release is the primary unit for overall runtime inference.
Repeated timings within a release are measurement replicates rather
than independent software-system observations.
"""

from __future__ import annotations

from math import comb
from typing import Iterable

import numpy as np
import pandas as pd


def runtime_reduction_percent(
    full_seconds: float,
    reduced_seconds: float,
) -> float:
    """Percentage runtime reduction relative to the full suite."""

    if full_seconds <= 0:
        raise ValueError("full_seconds must be > 0")

    return (
        100.0
        * (full_seconds - reduced_seconds)
        / full_seconds
    )


def speedup(
    full_seconds: float,
    reduced_seconds: float,
) -> float:
    """Full-suite runtime divided by reduced-suite runtime."""

    if reduced_seconds <= 0:
        raise ValueError("reduced_seconds must be > 0")

    return full_seconds / reduced_seconds


def release_runtime_statistics(
    paired: pd.DataFrame,
) -> pd.DataFrame:
    """
    Derive frozen release-level runtime statistics.

    Standard deviations use sample SD (ddof=1), matching the frozen
    analysis.
    """

    required = {
        "project",
        "version",
        "repetition",
        "full_seconds",
        "reduced_seconds",
    }

    missing = required - set(paired.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    rows = []

    for (project, version), g in paired.groupby(
        ["project", "version"],
        sort=False,
    ):

        full = g["full_seconds"].astype(float)
        reduced = g["reduced_seconds"].astype(float)

        full_median = float(full.median())
        reduced_median = float(reduced.median())

        pair_reductions = (
            100.0
            * (full - reduced)
            / full
        )

        rows.append({
            "project": project,
            "version": str(version),

            "full_mean_seconds":
                float(full.mean()),

            "full_median_seconds":
                full_median,

            "full_sd_seconds":
                float(full.std(ddof=1)),

            "reduced_mean_seconds":
                float(reduced.mean()),

            "reduced_median_seconds":
                reduced_median,

            "reduced_sd_seconds":
                float(reduced.std(ddof=1)),

            "median_runtime_reduction_pct":
                runtime_reduction_percent(
                    full_median,
                    reduced_median,
                ),

            "median_speedup":
                speedup(
                    full_median,
                    reduced_median,
                ),

            "paired_mean_runtime_reduction_pct":
                float(pair_reductions.mean()),

            "reduced_faster_pairs":
                int((reduced < full).sum()),

            "total_pairs":
                int(len(g)),
        })

    return pd.DataFrame(rows)


def project_runtime_statistics(
    release_stats: pd.DataFrame,
) -> pd.DataFrame:
    """Aggregate release-level runtime effects by project."""

    rows = []

    for project, g in release_stats.groupby(
        "project",
        sort=False,
    ):

        reductions = (
            g["median_runtime_reduction_pct"]
            .astype(float)
        )

        speedups = (
            g["median_speedup"]
            .astype(float)
        )

        rows.append({
            "project": project,
            "releases": int(len(g)),

            "mean_median_runtime_reduction_pct":
                float(reductions.mean()),

            "median_runtime_reduction_pct":
                float(reductions.median()),

            "min_runtime_reduction_pct":
                float(reductions.min()),

            "max_runtime_reduction_pct":
                float(reductions.max()),

            "median_speedup":
                float(speedups.median()),
        })

    return pd.DataFrame(rows)


def exact_two_sided_sign_test_p(
    positive: int,
    negative: int,
) -> float:
    """
    Exact two-sided sign-test p-value under p=0.5.

    Ties should be excluded before supplying positive and negative
    counts.
    """

    if positive < 0 or negative < 0:
        raise ValueError("Counts must be non-negative")

    n = positive + negative

    if n == 0:
        return 1.0

    k = min(positive, negative)

    tail = sum(
        comb(n, i)
        for i in range(k + 1)
    ) / (2 ** n)

    return min(
        1.0,
        2.0 * tail,
    )


def overall_runtime_statistics(
    release_stats: pd.DataFrame,
    paired: pd.DataFrame,
) -> dict:
    """
    Compute deterministic overall runtime statistics that do not
    require bootstrap resampling.
    """

    reductions = (
        release_stats[
            "median_runtime_reduction_pct"
        ].astype(float)
    )

    speedups = (
        release_stats[
            "median_speedup"
        ].astype(float)
    )

    positive = int(
        (reductions > 0).sum()
    )

    negative = int(
        (reductions < 0).sum()
    )

    return {
        "mean_release_level_median_reduction_percent":
            float(reductions.mean()),

        "median_release_level_median_reduction_percent":
            float(reductions.median()),

        "positive_releases":
            positive,

        "negative_releases":
            negative,

        "exact_sign_test_two_sided_p":
            exact_two_sided_sign_test_p(
                positive,
                negative,
            ),

        "reduced_faster_measurement_pairs":
            int(
                (
                    paired["reduced_seconds"].astype(float)
                    <
                    paired["full_seconds"].astype(float)
                ).sum()
            ),

        "total_measurement_pairs":
            int(len(paired)),

        "median_release_level_speedup":
            float(speedups.median()),
    }


def reduction_runtime_relationship(
    release_table: pd.DataFrame,
) -> dict:
    """
    Correlation between test-count reduction and runtime reduction.

    The input must contain one row per release.
    """

    required = {
        "test_count_reduction_pct",
        "median_runtime_reduction_pct",
    }

    missing = required - set(release_table.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    x = (
        release_table["test_count_reduction_pct"]
        .astype(float)
    )

    y = (
        release_table["median_runtime_reduction_pct"]
        .astype(float)
    )

    pearson = float(
        x.corr(y, method="pearson")
    )

    # Spearman correlation is Pearson correlation of ranks.
    # Implemented directly to avoid requiring SciPy.
    x_rank = x.rank(
        method="average"
    )

    y_rank = y.rank(
        method="average"
    )

    spearman = float(
        x_rank.corr(
            y_rank,
            method="pearson",
        )
    )

    return {
        "pearson_test_reduction_vs_runtime_reduction":
            pearson,

        "spearman_test_reduction_vs_runtime_reduction":
            spearman,
    }
