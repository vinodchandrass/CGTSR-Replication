# Environment and Dependency Provenance

## 1. Purpose

This file distinguishes dependencies required by the public reference
implementations from historical software versions retained in the
empirical study evidence.

A package version is not presented as a universal study-wide pin unless
the retained evidence supports that interpretation.

## 2. Public Reference Implementations

The public code under `src/cgtsr/` contains:

- `reduction.py` — Python standard library only;
- `baseline.py` — Python standard library plus the reduction module;
- `analysis.py` — Python standard library plus pandas.

The public CLI scripts use the same dependencies.

`requirements.txt` therefore declares `pandas` without inventing an
unsupported historical version pin.

## 3. Python Version Evidence

The retained Tier-3 evidence explicitly records Python 3.12.

Accordingly, Python 3.12 is the documented reference Python generation
for this replication package.

## 4. Historical Coverage Environment Evidence

The retained corrected coverage-characterization notebook explicitly
records the following environment for a cattrs 24.1.0 validation path:

- Python 3.12;
- pytest 8.0.0;
- coverage 7.4.0;
- pytest-cov 5.0.0.

These versions are historical provenance for that retained workflow.
They should not be interpreted as a universal dependency lock for every
subject release.

## 5. Additional pytest Version Evidence

The frozen Tier-3 baseline matrix also contains evidence for:

- Python 3.12;
- pytest 7.4.4.

The presence of both pytest 7.4.4 and pytest 8.0.0 in retained study
evidence indicates that subject/release environments were not represented
by one universal pytest version.

For that reason this repository does not collapse the historical
environments into a single fabricated pytest pin.

## 6. coverage.py and pytest-cov

Explicit retained version evidence includes:

- coverage 7.4.0;
- pytest-cov 5.0.0.

These values are retained as provenance for the corrected coverage
workflow in which they were recorded.

## 7. pandas

`src/cgtsr/analysis.py` requires pandas for tabular deterministic
analysis.

The exact historical pandas version used when the frozen empirical
statistics were originally generated was not found in the retained
version evidence.

Therefore:

- pandas is declared as a public reference-code dependency;
- no historical pandas version is fabricated;
- deterministic reference validation against the frozen results provides
  the repository-level correctness check.

## 8. Fresh Subject Execution

Users attempting fresh coverage characterization or subject-suite
execution should consult:

- `metadata/frozen_protocol/tier3_frozen_baseline_matrix.csv`;
- `metadata/frozen_protocol/tier3_frozen_per_test_coverage_protocol.json`;
- `scripts/Testing_Tier3_Corrected.ipynb`;
- `docs/REPRODUCIBILITY.md`.

Fresh subject execution should not assume that `requirements.txt` is a
complete recreation of every historical subject environment.

## 9. Reproducibility Boundary

`requirements.txt` supports the public reference-analysis code.

Historical subject environments are documented separately because
reproducibility metadata should preserve known differences rather than
replace them with unsupported uniform version assumptions.
