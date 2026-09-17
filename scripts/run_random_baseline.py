#!/usr/bin/env python
"""
CGTSR size-matched random baseline CLI.

Reference reproduction implementation reconstructed from the frozen
protocol and artifacts.

Protocol:
- combined statement + branch coverage
- lexicographically sorted test population
- Python random.Random(release_seed)
- one persistent RNG stream per release
- sampling without replacement
- each random subset has the same size as the corresponding
  CGTSR combined reduced suite

This script operates only on an existing per-test coverage JSON.
It does not execute pytest, coverage.py, subject code, or tests.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC = REPO_ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


from cgtsr.baseline import (  # noqa: E402
    run_size_matched_random_baseline,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run the CGTSR size-matched uniform random "
            "test-selection baseline."
        )
    )

    parser.add_argument(
        "coverage_json",
        type=Path,
        help="Per-test coverage-elements JSON.",
    )

    parser.add_argument(
        "--sample-size",
        type=int,
        required=True,
        help=(
            "Number of tests sampled in every trial. "
            "Use the corresponding combined CGTSR "
            "selected-suite size."
        ),
    )

    parser.add_argument(
        "--seed",
        type=int,
        required=True,
        help="Release-specific random seed.",
    )

    parser.add_argument(
        "--repetitions",
        type=int,
        default=1000,
        help="Number of random trials. Default: 1000.",
    )

    parser.add_argument(
        "--output-json",
        type=Path,
        default=None,
        help="Optional JSON output path.",
    )

    parser.add_argument(
        "--output-csv",
        type=Path,
        default=None,
        help="Optional trial-level CSV output path.",
    )

    return parser.parse_args()


def load_coverage(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(
            f"Coverage JSON not found: {path}"
        )

    data = json.loads(
        path.read_text(encoding="utf-8")
    )

    if not isinstance(data, dict):
        raise ValueError(
            "Coverage JSON must be an object keyed "
            "by pytest test IDs."
        )

    return data


def trial_to_dict(trial) -> dict:
    """
    Convert the validated RandomTrial result into a JSON/CSV-safe
    dictionary without assuming dataclasses.asdict semantics.
    """
    result = {}

    for name in (
        "trial",
        "sample_size",
        "covered_elements",
        "retention_percent",
    ):
        if hasattr(trial, name):
            result[name] = getattr(trial, name)

    # Preserve any actual public fields exposed by the implementation.
    if hasattr(trial, "__dict__"):
        for key, value in trial.__dict__.items():
            result.setdefault(key, value)

    return result


def main() -> int:
    args = parse_args()

    coverage = load_coverage(
        args.coverage_json
    )

    if args.sample_size < 1:
        raise ValueError(
            "--sample-size must be >= 1"
        )

    if args.sample_size > len(coverage):
        raise ValueError(
            "--sample-size cannot exceed the number "
            "of input test records."
        )

    if args.repetitions < 1:
        raise ValueError(
            "--repetitions must be >= 1"
        )

    trials = run_size_matched_random_baseline(
        coverage,
        sample_size=args.sample_size,
        release_seed=args.seed,
        repetitions=args.repetitions,
    )

    trial_rows = [
        trial_to_dict(t)
        for t in trials
    ]

    output = {
        "method":
            "size_matched_uniform_random_test_selection",

        "criterion":
            "combined_statement_branch",

        "sampling":
            "without_replacement",

        "population_order":
            "lexicographically_sorted_test_ids",

        "rng":
            "python_random.Random",

        "persistent_rng_stream":
            True,

        "input_test_records":
            len(coverage),

        "sample_size":
            args.sample_size,

        "release_seed":
            args.seed,

        "repetitions":
            args.repetitions,

        "trials":
            trial_rows,
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

    if args.output_csv is not None:
        args.output_csv.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if trial_rows:
            fieldnames = list(
                trial_rows[0].keys()
            )

            with args.output_csv.open(
                "w",
                newline="",
                encoding="utf-8",
            ) as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=fieldnames,
                )

                writer.writeheader()
                writer.writerows(trial_rows)

        print(
            f"CSV written to: {args.output_csv}"
        )

    print(
        f"Input tests       : {len(coverage)}"
    )
    print(
        f"Sample size       : {args.sample_size}"
    )
    print(
        f"Release seed      : {args.seed}"
    )
    print(
        f"Repetitions       : {args.repetitions}"
    )
    print(
        f"Generated trials  : {len(trials)}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
