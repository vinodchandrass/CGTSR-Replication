# Code provenance

## Frozen empirical evidence

The files under `results/` and the frozen protocol metadata are the
authoritative empirical record of the study.

The Tier-3 coverage-characterization notebook is retained under
`scripts/` as sanitized provenance from the original experimental
workflow.

## CGTSR reference implementation

The later transient code used to perform CGTSR reduction, the
size-matched random baseline, runtime benchmarking, and final
statistical freeze was not found as a persisted Python script or
notebook in the archived workspace.

Accordingly, code under `src/cgtsr/` is explicitly provided as a
**reference reproduction implementation** reconstructed from the
frozen protocol and empirical artifacts. It must not be interpreted
as the original transient execution script.

The reference implementation is intended to permit independent
verification of the documented method against the frozen inputs and
outputs.

## Methodological boundary

CGTSR is a deterministic greedy coverage-preserving reduction method.
It preserves the observed frozen coverage universe for the selected
coverage criterion. It does not establish global minimum-cardinality
test suites and does not establish equivalent fault-detection
effectiveness.


## Statistical-bootstrap provenance

The frozen empirical results report release-level bootstrap confidence
intervals for the mean and median release-level runtime reductions.

The retained frozen values are:

- mean release-level median runtime reduction:
  43.540355891085916%, with frozen 95% release-bootstrap CI
  [25.38839298132632%, 61.249284088655536%];

- median release-level median runtime reduction:
  48.505865834318946%, with frozen 95% release-bootstrap CI
  [8.532724341831878%, 74.92927725233442%].

A provenance search of the retained workspace found no persisted
statistical-bootstrap execution implementation containing the original
resampling count, random-number-generator configuration or seed, and
confidence-interval calculation procedure.

Occurrences of the term `bootstrap` in the retained Tier-3 notebook
refer to Python packaging/environment bootstrapping (for example,
installing or upgrading pip, setuptools, and wheel), not statistical
bootstrap resampling.

Accordingly, `src/cgtsr/analysis.py` reproduces the deterministic
statistical analysis from the frozen measurements but does not claim
exact procedural reproduction of the frozen bootstrap confidence
intervals.

The frozen confidence intervals remain authoritative empirical
artifacts. No undocumented seed, resampling count, RNG implementation,
or percentile convention is inferred merely to reproduce those
numerical endpoints.
