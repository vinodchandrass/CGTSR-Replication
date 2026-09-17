#!/usr/bin/env python
"""
CGTSR deterministic greedy coverage-preserving reduction.

This command-line interface operates on an existing frozen per-test
coverage JSON file. It does not execute pytest, coverage.py, subject
source code, or test suites.

The implementation is a reference reproduction implementation
reconstructed from the frozen protocol and artifacts. It must not be
interpreted as the original transient execution script.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC = REPO_ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


from cgtsr.reduction import (  # noqa: E402
    greedy_reduce,
)


VALID_CRITERIA = (
    "statement",
    "branch",
    "combined",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run deterministic greedy coverage-preserving "
            "test-suite reduction on a per-test coverage JSON."
        )
    )

    parser.add_argument(
        "coverage_json",
        type=Path,
        help=(
            "Path to per_test_coverage_elements JSON."
        ),
    )

    parser.add_argument(
        "--criterion",
        choices=VALID_CRITERIA,
        default="combined",
        help=(
            "Coverage criterion. Default: combined."
        ),
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help=(
            "Optional output JSON path. If omitted, the "
            "result is printed only."
        ),
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
            "Coverage JSON must contain an object keyed "
            "by pytest test IDs."
        )

    return data


def main() -> int:
    args = parse_args()

    coverage = load_coverage(
        args.coverage_json
    )

    result = greedy_reduce(
        coverage,
        criterion=args.criterion,
    )

    output = {
        "method":
            "deterministic_greedy_coverage_preserving_reduction",

        "criterion":
            args.criterion,

        "input_test_records":
            len(coverage),

        "coverage_universe_size":
            result.coverage_elements,

        "selected_test_count":
            result.selected_count,

        "selected_tests":
            result.selected_tests,

        "coverage_preserved":
            result.coverage_preserved,

        "interpretive_boundary":
            (
                "Greedy coverage-preserving reduction does "
                "not establish globally minimal suite size "
                "or equivalent fault-detection effectiveness."
            ),
    }

    text = json.dumps(
        output,
        indent=2,
    )

    if args.output is not None:
        args.output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        args.output.write_text(
            text + "\n",
            encoding="utf-8",
        )

        print(
            f"Result written to: {args.output}"
        )

    print(
        f"Criterion             : {args.criterion}"
    )
    print(
        f"Input tests           : {len(coverage)}"
    )
    print(
        f"Coverage universe     : {result.coverage_elements}"
    )
    print(
        f"Selected tests        : {result.selected_count}"
    )
    print(
        f"Coverage preserved    : {result.coverage_preserved}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
