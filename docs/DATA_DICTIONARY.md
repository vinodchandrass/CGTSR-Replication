# Data Dictionary

## 1. Purpose

This document describes the principal public data, result, validation,
and metadata artifacts in the CGTSR reproducibility package.

Frozen empirical artifacts should be treated as immutable evidence.

## 2. Selected-Test Data

### `data/selected_tests/<project>/<version>/selected_tests_<criterion>.txt`

There are 36 selected-test files: 12 releases x 3 criteria.

Each file contains the pytest test identifiers selected by the
deterministic greedy coverage-preserving reduction procedure.

Criteria:

- `statement`: statement-coverage reduction;
- `branch`: branch-arc reduction;
- `combined`: namespaced statement + branch reduction.

Selection order is significant because deterministic tie-breaking is
part of the reproducibility protocol.

## 3. Normalization Metadata

### `data/normalization/attrs_24.1.0_normalization_manifest.json`

Documents denominator normalization for attrs 24.1.0.

Important fields:

- `project`: subject project;
- `version`: subject release;
- `purpose`: reason for normalization;
- `original_element_records`: original attributed records;
- `collected_tests_without_context_added`: explicit empty records added;
- `normalized_records`: final denominator;
- `zero_coverage_records`: zero-coverage records;
- `frozen_tier3_input_modified`: whether original frozen input changed;
- `normalization_rule`: normalization policy.

## 4. Coverage Characterization

### `results/coverage_characterization/tier3_per_test_coverage_summary.csv`

One row per project release; 12 rows total.

| Column | Meaning |
|---|---|
| project | Subject project |
| version | Release version |
| status | Coverage-characterization status |
| collected_tests | pytest-collected test count |
| coverage_context_tests | Tests represented by dynamic coverage contexts |
| tests_without_coverage_context | Collected tests without attributed context |
| unexpected_context_ids | Unexpected dynamic context identifiers |
| production_files | Production source files represented |
| tests_with_statement_coverage | Tests with attributed statement coverage |
| tests_with_branch_arc_coverage | Tests with attributed branch-arc coverage |
| observed_statement_elements | Observed production statement universe size |
| observed_branch_arc_elements | Observed production branch-arc universe size |
| coverage_runtime_seconds | Coverage-characterization runtime |

The corresponding JSON contains protocol metadata and release-level
results in structured form.

## 5. CGTSR Reduction Results

### `results/cgtsr_reduction/cgtsr_reduction_summary.csv`

Contains 36 rows: 12 releases x 3 reduction criteria.

| Column | Meaning |
|---|---|
| project | Subject project |
| version | Release version |
| criterion | statement, branch, or combined |
| original_tests | Input test denominator |
| selected_tests | Number selected by CGTSR |
| removed_tests | original_tests - selected_tests |
| reduction_percent | Percentage reduction in test count |
| coverage_elements | Size of the criterion-specific frozen universe |
| coverage_preserved | Whether the selected suite covers the complete frozen universe |

The JSON version additionally records method, tie-breaking policy,
criteria, denominator policy, normalization, and result records.

## 6. Random-Baseline Summary

### `results/random_baseline/cgtsr_random_baseline_summary.csv`

One row per release; 12 rows total.

| Column | Meaning |
|---|---|
| project | Subject project |
| version | Release version |
| original_tests | Release test denominator |
| sample_size | Number of tests in every random subset |
| universe_elements | Combined frozen coverage-universe size |
| cgtsr_retention_percent | CGTSR combined coverage retention |
| random_mean_retention_percent | Mean random coverage retention |
| random_median_retention_percent | Median random retention |
| random_sd_retention_percent | Standard deviation across random trials |
| random_p2_5_percent | 2.5th percentile of random retention |
| random_p97_5_percent | 97.5th percentile of random retention |
| random_min_percent | Minimum random retention |
| random_max_percent | Maximum random retention |
| random_full_coverage_trials | Number of random subsets attaining full coverage |
| empirical_p_full_coverage | Smoothed empirical full-coverage probability estimate |
| repetitions | Number of random trials |
| release_seed | Release-specific RNG seed |

The empirical full-coverage value is a random-baseline probability
estimate under the specified sampling protocol; it should not be
described as a general hypothesis-test p-value.

## 7. Random-Baseline Trial Data

### `results/random_baseline/cgtsr_random_baseline_trials.csv`

Contains 12,000 rows: 1,000 trials for each of 12 releases.

| Column | Meaning |
|---|---|
| project | Subject project |
| version | Release version |
| trial | Trial number within release |
| seed | Release-specific RNG seed |
| original_tests | Test population size |
| sample_size | Size-matched random subset size |
| universe_elements | Combined frozen coverage-universe size |
| covered_elements | Universe elements covered by the random subset |
| retention_percent | Percentage of the combined universe retained |

## 8. Reduced-Suite Execution Validation

### `results/execution_validation/`

Records execution validation for the 12 combined selected suites.

`attrs/24.1.0/combined_reduced_execution.json` contains the attrs 24.1.0
pilot execution record.

`remaining_11_execution_summary.csv` contains the remaining 11 releases.

Important CSV fields include project, version, selected test count,
exit code, status, wall-clock time, pytest summary, repository/environment
provenance, and timestamps.

These artifacts demonstrate that all 12 selected combined suites were
executable and passed under the study environments.

## 9. Runtime Benchmark Summary

### `results/runtime/final_runtime_summary_12_releases.csv`

One row per release.

Important fields:

- `selected_tests`: combined reduced-suite size;
- `measured_repetitions_per_suite`: measured timing repetitions;
- `warmup_runs_per_suite`: warm-up count;
- `execution_order`: full/reduced ordering protocol;
- `coverage_instrumentation`: whether coverage was active;
- `full_mean_seconds`, `full_median_seconds`: full-suite timing;
- `reduced_mean_seconds`, `reduced_median_seconds`: reduced-suite timing;
- `median_runtime_reduction_percent`: primary release-level runtime effect;
- `median_speedup`: full median divided by reduced median;
- `full_stdev_seconds`, `reduced_stdev_seconds`: timing dispersion;
- `paired_mean_runtime_reduction_percent`: mean paired timing reduction;
- `all_exit_codes_zero`: execution-integrity indicator.

## 10. Paired Runtime Measurements

### `results/final_empirical_freeze/paired_runtime_measurements.csv`

Contains 60 rows: 12 releases x 5 measured repetitions.

| Column | Meaning |
|---|---|
| project | Subject project |
| version | Release version |
| repetition | Measured repetition number |
| full_seconds | Full-suite runtime |
| reduced_seconds | Reduced-suite runtime |
| difference_seconds | Full minus reduced runtime |
| runtime_reduction_pct | Paired runtime reduction percentage |
| speedup | Full runtime divided by reduced runtime |
| reduced_faster | Whether reduced runtime was lower |

Repeated timing measurements within a release are measurement replicates,
not independent software-system observations.

## 11. Release-Level Runtime Statistics

### `results/final_empirical_freeze/release_runtime_statistics.csv`

Contains 12 release-level rows.

Fields include full/reduced means, medians, sample standard deviations,
median runtime reduction, median speedup, paired mean reduction, and
the number of reduced-faster measurement pairs.

## 12. Project-Level Runtime Statistics

### `results/final_empirical_freeze/project_runtime_statistics.csv`

Contains four project-level rows.

Fields summarize the mean, median, minimum, and maximum release-level
median runtime reductions and the median release-level speedup.

## 13. Paper-Ready Tables

### `paper_table_release_level.csv`

Contains 12 rows combining reduction, structural coverage, random-baseline,
and runtime outcomes for manuscript reporting.

### `paper_table_project_level.csv`

Contains four rows summarizing pooled test-count reduction and runtime
effects by project.

## 14. Selected-Test Integrity

### `results/final_empirical_freeze/selected_test_integrity.csv`

One row per release with:

- expected selected count;
- actual selected count;
- duplicate count;
- integrity status.

## 15. Random-Baseline Reference Table

### `results/final_empirical_freeze/random_baseline_reference.csv`

One row per release comparing CGTSR combined coverage with mean random
coverage and the number of full-coverage random trials.

## 16. Claim-Safety Audit

### `results/final_empirical_freeze/claim_safety_audit.csv`

Contains eight claim-level records with:

- `claim`: empirical or methodological claim;
- `supported`: support status;
- `scope`: permitted interpretation.

This file helps prevent claims from extending beyond the empirical design.

## 17. Final Empirical Summary

### `results/final_empirical_freeze/final_empirical_summary.json`

Machine-readable summary of the frozen empirical analysis, including
project/release counts, pooled reduction, coverage preservation, random
baseline results, runtime protocol, runtime statistics, correlation
results, and limitations.

## 18. Final Freeze Manifest

### `results/final_empirical_freeze/CGTSR_FINAL_FREEZE_MANIFEST.json`

Records freeze status, protocol status, criteria, primary criterion,
aggregate counts, coverage preservation, random-baseline trial count,
execution/runtime validation status, hashes, and claim boundaries.

## 19. Reference-Implementation Validation

### `results/reference_validation/`

Contains JSON and human-readable TXT evidence for:

- deterministic reduction reference validation;
- random-baseline reference validation;
- deterministic analysis reference validation.

These artifacts distinguish reconstructed reference code from original
execution provenance and record the degree of exact agreement with the
frozen empirical evidence.

## 20. Subject and Protocol Metadata

### `metadata/subject_releases.csv`

Contains the 12 project/version identities.

### `metadata/frozen_protocol/tier3_frozen_baseline_matrix.csv`

Records release-level baseline environment and eligibility information.

### `metadata/frozen_protocol/tier3_frozen_per_test_coverage_protocol.json`

Records the frozen coverage-characterization protocol, test-universe
policy, zero-coverage policy, scope rules, and integrity policy.

## 21. Build and Portability Metadata

`metadata/production_build_manifest.json`,
`metadata/portability_cleanup_manifest.json`, and
`metadata/frozen_evidence_addition_manifest.json` document construction
of the publication package without altering the original frozen workspace.

The private `_pre_portability_cleanup` backup is staging material and is
not part of the intended public GitHub release. It must be removed during
the final repository preflight.

## 22. Interpretation Boundary

The data establish preservation of the represented frozen structural
coverage universe. They do not establish globally minimal suite size or
equivalent fault-detection effectiveness.
