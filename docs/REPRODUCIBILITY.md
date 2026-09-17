# Reproducibility Guide

## 1. Scope

This repository provides the reproducibility package for the empirical
evaluation of deterministic greedy coverage-preserving test-suite
reduction (CGTSR) across 12 releases of four open-source Python projects.

The package distinguishes between frozen empirical evidence, retained
coverage-characterization provenance, and reference reproduction
implementations reconstructed from the frozen protocol and artifacts.

Code under `src/cgtsr/` is reference reproduction code where the original
later-stage transient execution scripts were not retained.

## 2. Empirical Subjects

| Project | Releases |
|---|---|
| attrs | 24.1.0, 25.3.0, 26.1.0 |
| cattrs | 24.1.0, 25.3.0, 26.1.0 |
| boltons | 24.1.0, 25.0.0, 26.1.0 |
| more-itertools | 10.5.0, 10.8.0, 11.1.0 |

Release metadata is retained in `metadata/subject_releases.csv`.

## 3. Coverage Characterization

Coverage characterization used pytest, coverage.py, branch coverage,
and dynamic test contexts.

Per-test production coverage was represented using executed statements
and executed branch arcs. Combined reduction keeps statement and branch
elements in separate namespaces.

The retained coverage-characterization notebook is:

`scripts/Testing_Tier3_Corrected.ipynb`

Its publication copy has machine-specific paths sanitized and outputs
cleared. It is retained as methodological provenance.

The frozen protocol is under `metadata/frozen_protocol/`.

## 4. attrs 24.1.0 Normalization

pytest collection contained 1,334 tests for attrs 24.1.0, while the
original per-test coverage artifact contained 1,260 context-attributed
tests. The remaining 74 collected tests were represented as explicit
empty coverage records for the CGTSR denominator.

Thus:

- collected tests: 1,334;
- context-attributed records: 1,260;
- empty records added: 74;
- normalized records: 1,334.

The original frozen Tier-3 input was not modified.

See `data/normalization/attrs_24.1.0_normalization_manifest.json`.

## 5. Deterministic Greedy Reduction

Reference implementation: `src/cgtsr/reduction.py`

Public CLI: `scripts/run_reduction.py`

For each criterion, the algorithm repeatedly selects the test with the
largest marginal gain over the currently uncovered structural universe.
Equal-gain ties are resolved by the lexicographically smallest pytest
test identifier. Selection continues until the frozen universe is covered.

Supported criteria are statement, branch, and combined statement+branch.

The correct description is **deterministic greedy coverage-preserving
reduction**. It is not a claim of globally minimal suite size.

Example:

```bash
python scripts/run_reduction.py COVERAGE_JSON --criterion combined --output reduction.json
```

The reference implementation reproduced all 36 frozen release-by-criterion
selections exactly, including selection order.

## 6. Size-Matched Random Baseline

Reference implementation: `src/cgtsr/baseline.py`

Public CLI: `scripts/run_random_baseline.py`

Frozen protocol:

- combined statement+branch criterion;
- uniform sampling without replacement;
- sample size equal to the corresponding CGTSR selected-suite size;
- lexicographically sorted pytest test population;
- Python `random.Random(release_seed)`;
- one persistent RNG stream per release;
- 1,000 repetitions per release;
- release seeds 20260915 through 20260926.

Example:

```bash
python scripts/run_random_baseline.py COVERAGE_JSON --sample-size 190 --seed 20260915 --repetitions 1000 --output-json baseline.json
```

The reference implementation reproduced 12,000/12,000 frozen random
baseline trials exactly.

## 7. Deterministic Runtime Analysis

Reference implementation: `src/cgtsr/analysis.py`

Public CLI: `scripts/analyze_results.py`

The analysis CLI reads frozen timing measurements. It does not rerun
runtime benchmarks.

Example:

```bash
python scripts/analyze_results.py --freeze-dir results/final_empirical_freeze --output-json reconstructed_analysis.json
```

Validated deterministic results include:

- mean release-level median runtime reduction: 43.540355891085916%;
- median release-level median runtime reduction: 48.505865834318946%;
- positive release effects: 12/12;
- exact two-sided release-level sign-test p = 0.00048828125;
- reduced-faster measurement pairs: 59/60;
- median release-level speedup: 2.187004552509833;
- Pearson correlation: 0.9715916529567671;
- Spearman correlation: 0.7342657342657343.

The five timing repetitions within each release are repeated measurements,
not independent software-system replicates. The release is the primary
unit for overall inference.

## 8. Bootstrap Confidence Intervals

The frozen empirical results contain 95% bootstrap confidence intervals
for the mean and median release-level runtime reductions.

The original transient statistical-bootstrap implementation was not
retained. Its exact resample count, RNG implementation, seed, and
percentile/quantile implementation are therefore not inferred.

The frozen intervals are retained as authoritative empirical results but
are not claimed to be procedurally regenerated by the public code.

See `docs/CODE_PROVENANCE.md`.

## 9. Frozen Empirical Results

The principal frozen package is `results/final_empirical_freeze/`.

For the combined reduction:

- original test instances: 10,129;
- selected test instances: 2,381;
- removed test instances: 7,748;
- pooled test-count reduction: 76.49323723960904%;
- frozen combined structural coverage preservation: 100%.

All 12 combined selected suites were also executed successfully during
the empirical study.

## 10. Interpretation Boundaries

Structural coverage preservation does not establish globally minimal
suite size, equivalent fault-detection effectiveness, equivalent mutation
score, or semantic equivalence between the full and reduced suites.

None of the 12,000 size-matched random samples preserved the complete
frozen combined structural universe. This supports nontrivial selection
quality relative to the specified random baseline; it does not prove
global optimization-theoretic optimality.

## 11. Reproduction Levels

**Level A — Frozen-result inspection:** inspect `results/` without
executing empirical experiments.

**Level B — Deterministic reference reproduction:** use
`run_reduction.py`, `run_random_baseline.py`, and `analyze_results.py`.

**Level C — Coverage-characterization provenance:** consult the retained
Tier-3 notebook and frozen protocol metadata before attempting fresh
subject execution.

## 12. Evidence-Preservation Principle

Frozen empirical artifacts are treated as immutable evidence.

Reference implementations are validated against those artifacts rather
than silently replacing them. Where original transient code was not
retained, the repository states that provenance limitation explicitly.
