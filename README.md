# CGTSR Replication Package

## Deterministic Greedy Coverage-Preserving Test-Suite Reduction

This repository provides the reproducibility package for an empirical
study of coverage-guided test-suite reduction across multiple releases
of open-source Python software projects.

The repository contains frozen empirical evidence, selected test suites,
random-baseline results, runtime measurements, protocol metadata, and
validated reference implementations for reproducing the principal
deterministic analyses.

## Study Scope

The Tier-3 empirical evaluation covers four projects and 12 releases:

| Project | Releases |
|---|---|
| attrs | 24.1.0, 25.3.0, 26.1.0 |
| cattrs | 24.1.0, 25.3.0, 26.1.0 |
| boltons | 24.1.0, 25.0.0, 26.1.0 |
| more-itertools | 10.5.0, 10.8.0, 11.1.0 |

The primary reduction criterion is combined statement + branch coverage.

## Method

For each release, the reduction procedure operates on frozen per-test
structural coverage sets.

At each iteration it selects the remaining test with the largest
marginal gain over the uncovered coverage universe. Equal-gain ties are
resolved using the lexicographically smallest pytest test identifier.

Selection continues until the complete represented coverage universe is
covered.

The method is therefore described as:

**deterministic greedy coverage-preserving reduction**

The greedy procedure does not establish global minimum suite size.

## Principal Frozen Results

For the combined statement + branch criterion across the 12 releases:

- original test instances: **10,129**;
- selected test instances: **2,381**;
- removed test instances: **7,748**;
- pooled test-count reduction: **76.49%**;
- represented structural coverage preserved: **100%**.

All 12 combined selected suites were executed successfully under the
study environments.

### Random Baseline

The study evaluated 1,000 size-matched random subsets for each release,
giving **12,000 random trials** in total.

None of the 12,000 random subsets preserved the complete combined frozen
structural coverage universe.

The validated reference baseline implementation reproduces all
**12,000/12,000 frozen trial records exactly**.

### Runtime

Using the release as the primary analysis unit:

- mean release-level median runtime reduction: **43.54%**;
- median release-level median runtime reduction: **48.51%**;
- positive release-level runtime effects: **12/12**;
- exact two-sided release-level sign-test p: **0.00048828125**;
- reduced-faster measured timing pairs: **59/60**;
- median release-level speedup: **2.187x**.

Test-count reduction and runtime reduction were positively associated:

- Pearson correlation: **0.9716**;
- Spearman correlation: **0.7343**.

Timing repetitions within a release are repeated measurements and are
not treated as independent software-system replicates.

## Repository Structure

```text
CGTSR_Replication/
|-- src/cgtsr/                 # validated reference implementations
|-- scripts/                   # public CLIs and retained notebook
|-- data/                      # selected tests and normalization metadata
|-- results/                   # frozen empirical and validation results
|-- metadata/                  # protocol and release metadata
|-- docs/                      # reproducibility/provenance documentation
|-- README.md
```

## Reference Implementations

The public reference implementations are:

- `src/cgtsr/reduction.py` — deterministic greedy reduction;
- `src/cgtsr/baseline.py` — size-matched random baseline;
- `src/cgtsr/analysis.py` — deterministic statistical analysis.

These implementations were reconstructed from the frozen protocol and
empirical artifacts where the original later-stage transient scripts
were not retained. They are not presented as the original transient
execution code.

Validation evidence is available under:

`results/reference_validation/`

## Quick Start

### 1. Reduction

```bash
python scripts/run_reduction.py COVERAGE_JSON --criterion combined --output reduction.json
```

### 2. Size-Matched Random Baseline

```bash
python scripts/run_random_baseline.py COVERAGE_JSON --sample-size 190 --seed 20260915 --repetitions 1000 --output-json baseline.json
```

The sample size and seed must correspond to the release being analyzed.

### 3. Deterministic Analysis of Frozen Runtime Results

```bash
python scripts/analyze_results.py --freeze-dir results/final_empirical_freeze --output-json reconstructed_analysis.json
```

This command analyzes frozen measurements. It does not rerun benchmarks.

## Reproducibility Levels

The package supports three levels of inspection/reproduction:

1. **Frozen-result inspection** — inspect the empirical artifacts under
   `results/` without executing experiments.
2. **Deterministic reference reproduction** — use the public reduction,
   random-baseline, and analysis CLIs.
3. **Coverage-characterization provenance** — inspect the retained
   Tier-3 notebook and frozen protocol metadata before attempting fresh
   subject execution.

For detailed instructions see:

- `docs/REPRODUCIBILITY.md`
- `docs/DATA_DICTIONARY.md`
- `docs/CODE_PROVENANCE.md`

## Important Interpretation Boundaries

The empirical evidence supports preservation of the represented frozen
structural coverage universe.

It does not by itself establish:

- globally minimal test-suite size;
- equivalent fault-detection effectiveness;
- equivalent mutation score;
- semantic equivalence of full and reduced suites;
- universal runtime improvement across arbitrary software systems.

The random baseline provides evidence that the deterministic greedy
selection is nontrivial relative to size-matched uniform random
selection. It is not evidence of global optimization-theoretic
optimality.

## Bootstrap Provenance

The frozen empirical analysis contains bootstrap confidence intervals
for the mean and median release-level runtime reductions.

The original transient statistical-bootstrap implementation was not
retained. Therefore its exact resample count, RNG/seed, and exact
percentile implementation are not reconstructed or inferred.

The frozen confidence intervals remain part of the empirical record,
but the public deterministic analysis code does not claim to regenerate
them procedurally.

See `docs/CODE_PROVENANCE.md` for details.

## Data and Evidence Integrity

Frozen empirical artifacts are treated as immutable evidence.

Reference implementations are validated against those artifacts rather
than used to silently replace or rewrite them.

## Documentation

- **Reproducibility:** `docs/REPRODUCIBILITY.md`
- **Data dictionary:** `docs/DATA_DICTIONARY.md`
- **Code provenance:** `docs/CODE_PROVENANCE.md`

## Citation

Citation metadata will be provided in `CITATION.cff`.

When using this repository, please cite the associated research article
and the archived/released version of this replication package when
available.
