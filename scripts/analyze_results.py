#!/usr/bin/env python
"""
CGTSR deterministic frozen-result analysis CLI.

This command reconstructs deterministic statistical results from
already-frozen empirical CSV artifacts.

It does NOT:
- execute subject tests;
- execute pytest;
- execute coverage.py;
- rerun runtime benchmarks;
- regenerate the original bootstrap confidence intervals.

The original statistical-bootstrap execution implementation was not
retained. Therefore the frozen bootstrap confidence intervals remain
authoritative artifacts and are reported as provenance-preserved
values rather than procedurally regenerated values.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC = REPO_ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


from cgtsr.analysis import (  # noqa: E402
    release_runtime_statistics,
    project_runtime_statistics,
    overall_runtime_statistics,
    reduction_runtime_relationship,
)


FROZEN_MEAN_BOOTSTRAP_CI = [
    25.38839298132632,
    61.249284088655536,
]

FROZEN_MEDIAN_BOOTSTRAP_CI = [
    8.532724341831878,
    74.92927725233442,
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Reconstruct deterministic CGTSR statistical "
            "analysis from frozen empirical result files."
        )
    )

    parser.add_argument(
        "--freeze-dir",
        type=Path,
        default=(
            REPO_ROOT
            / "results"
            / "final_empirical_freeze"
        ),
        help=(
            "Directory containing the frozen empirical "
            "result artifacts."
        ),
    )

    parser.add_argument(
        "--output-json",
        type=Path,
        default=None,
        help=(
            "Optional path for reconstructed deterministic "
            "analysis JSON."
        ),
    )

    return parser.parse_args()


def require_file(path: Path) -> Path:
    if not path.exists():
        raise FileNotFoundError(
            f"Required frozen artifact not found: {path}"
        )

    return path


def dataframe_records(
    df: pd.DataFrame
) -> list[dict]:
    """
    Convert a DataFrame to JSON-safe records.
    """
    return json.loads(
        df.to_json(
            orient="records",
            double_precision=15,
        )
    )


def main() -> int:
    args = parse_args()

    freeze = args.freeze_dir

    paired_path = require_file(
        freeze
        / "paired_runtime_measurements.csv"
    )

    release_table_path = require_file(
        freeze
        / "paper_table_release_level.csv"
    )

    paired = pd.read_csv(
        paired_path
    )

    release_table = pd.read_csv(
        release_table_path
    )

    # ------------------------------------------------------
    # Deterministic reconstruction
    # ------------------------------------------------------

    release_stats = (
        release_runtime_statistics(
            paired
        )
    )

    project_stats = (
        project_runtime_statistics(
            release_stats
        )
    )

    overall = (
        overall_runtime_statistics(
            release_stats,
            paired,
        )
    )

    relationship = (
        reduction_runtime_relationship(
            release_table
        )
    )

    output = {
        "analysis_type":
            "deterministic_frozen_result_reconstruction",

        "release_statistics":
            dataframe_records(
                release_stats
            ),

        "project_statistics":
            dataframe_records(
                project_stats
            ),

        "overall_runtime":
            overall,

        "relationship":
            relationship,

        "bootstrap_confidence_intervals": {
            "procedurally_recomputed":
                False,

            "reason":
                (
                    "The original statistical-bootstrap "
                    "execution implementation, including "
                    "resample count, RNG/seed, and exact CI "
                    "calculation procedure, was not retained."
                ),

            "frozen_mean_release_bootstrap_95_ci":
                FROZEN_MEAN_BOOTSTRAP_CI,

            "frozen_median_release_bootstrap_95_ci":
                FROZEN_MEDIAN_BOOTSTRAP_CI,

            "status":
                "provenance_preserved_not_regenerated",
        },

        "execution_boundary": {
            "subject_tests_executed":
                False,

            "pytest_executed":
                False,

            "coverage_executed":
                False,

            "runtime_benchmarks_rerun":
                False,
        },
    }

    if args.output_json is not None:
        args.output_json.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        args.output_json.write_text(
            json.dumps(
                output,
                indent=2,
            ) + "\n",
            encoding="utf-8",
        )

        print(
            f"JSON written to: {args.output_json}"
        )

    print(
        f"Release rows                 : "
        f"{len(release_stats)}"
    )

    print(
        f"Project rows                 : "
        f"{len(project_stats)}"
    )

    print(
        "Mean median-runtime reduction: "
        f"{overall['mean_release_level_median_reduction_percent']:.12f}%"
    )

    print(
        "Median runtime reduction     : "
        f"{overall['median_release_level_median_reduction_percent']:.12f}%"
    )

    print(
        "Positive releases            : "
        f"{overall['positive_releases']}"
    )

    print(
        "Exact sign-test p            : "
        f"{overall['exact_sign_test_two_sided_p']:.12f}"
    )

    print(
        "Reduced-faster pairs         : "
        f"{overall['reduced_faster_measurement_pairs']}/"
        f"{overall['total_measurement_pairs']}"
    )

    print(
        "Median release speedup       : "
        f"{overall['median_release_level_speedup']:.12f}"
    )

    print(
        "Pearson correlation          : "
        f"{relationship['pearson_test_reduction_vs_runtime_reduction']:.12f}"
    )

    print(
        "Spearman correlation         : "
        f"{relationship['spearman_test_reduction_vs_runtime_reduction']:.12f}"
    )

    print(
        "Bootstrap CI regeneration    : NO "
        "(frozen values preserved)"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
