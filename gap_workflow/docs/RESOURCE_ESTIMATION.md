# From a failed pilot to a resource decision

The workflow keeps four sizes separate: the number of physical sites, the full Hilbert dimension, the largest certified symmetry block, and the retained trial rank. An MPS bond dimension, when requested for storage planning, is a fifth quantity. None determines the others without a representation and a model.

## A concrete admission decision

The open spin-half 2 by 2 by 2 XXZ example has full dimension 256. Its exact magnetization sectors have dimensions 1, 8, 28, 56, 70, 56, 28, 8, and 1. An exact block cap of 32 is insufficient for exhaustive inertia coverage. A cap of 70 admits every block. The two example inputs differ only in this explicit budget. The larger cap is sufficient for this implementation, rather than a claim that no other certificate could use a smaller space.

The spin-one 2 by 2 square has full dimension 81 and largest magnetization sector 19. Exhaustive sector coverage fits the default exact cap of 32. Checking only the largest sector would not establish the full-model gap: all sectors are included and their dimensions sum to the full dimension.

## Measured cost and forecasts

The numerical pilots compute four low Ritz pairs for eleven small finite models. A separate exact benchmark uses two proposed low states and exact arithmetic to certify six finite-size bounds. Neither pilot replaces spectral completeness with a residual test. Exact certification covers the omitted states through inertia or a proved analytical tail.

`benchmarks/partial_spectrum_pilots.json` records measured construction, matrix-vector and partial-solve times. `benchmarks/resource_forecasts.json` contains 28 full-space/sector forecasts using the same Python matrix-free backend and an assumed 200 matrix-vector operations. These are estimates for that implementation and machine. A compiled backend, different hardware, or a different convergence rate requires new calibration.

For example, the spin-one 12-site chain has full dimension 531441 and Sz=0 dimension 73789. The current accounting estimates about 0.38 GiB and 0.053 GiB for their respective matrix-free iterative workspaces. The corresponding 200-operation forecasts are about 3234 s and 449 s. These estimates exclude an unproved guarantee of convergence and do not establish a useful bootstrap seed.

The spin-half 3 by 3 by 3 model has full dimension 134217728. Its smallest-|Sz| sector has dimension 20058300. The same Python representation estimates about 126 GiB and 18.8 GiB. This rules out these particular computations under the default 512 MiB budget. It does not rule out a tensor-network, analytical, or more specialized certificate.

## Predicting a seed size

`forecast_seed_size(records, threshold, max_size=None)` is a callable Python interface. The CLI does not currently call it or generate its records. The similarly named `benchmarks/resource_forecast.py` estimates computational costs through `plan_resources` and does not call this seed predictor.

Each record requires a distinct integer `linear_size >= 2`, `defect_upper` in (0,1], and an explicit `evidence` label of `certified_bound` or `floating_estimate`. Defects must also be representable as positive finite floats for the existing fit. The threshold lies in (0,1). Optional `max_size` is an integer at least 2 and is checked before any early return. It limits the proposed next computation, not the sizes of existing measurements.

### Sample provenance

Each record supplies its own `provenance` object with the five descriptors below. Every descriptor contains a nonempty string `id` and a JSON object `settings`. The certificate descriptor additionally requires `threshold`, expressed as an exact rational or decimal string. It must equal the function's threshold exactly.

| Descriptor | Meaning of the immutable definition and its settings |
| --- | --- |
| `model_family` | Hamiltonian family, spins, all fixed couplings and fields, energy normalization and shifts, and spectral or sector scope |
| `geometry_family` | Shape as a function of `linear_size`, dimension, boundaries, bond multiplicity, and the physical unit counted by `linear_size` |
| `temperature_protocol` | Fixed temperature or search grid, objective, search order, stopping rule, tolerances and implementation revision |
| `trial_rank_protocol` | Trial representation, fixed rank or size-dependent rank rule, search and stopping rules, tolerances and implementation revision |
| `certificate_criterion` | Defect definition, certificate version, normalization, target, inequality convention and all criterion parameters |

An `id` identifies an immutable definition, such as a versioned specification or a content hash of a complete manifest. A display name alone is insufficient. `settings` records its complete configuration, including explicitly resolved defaults. An empty object is appropriate only when the referenced definition has no adjustable settings. Exact physical parameters should use canonical rational strings. The validator checks declarations for agreement. It does not reconstruct a Hamiltonian from an ID, check that a manifest exists, or detect false or omitted settings inside a caller's declaration.

The descriptors are compared by value, including every nested setting. Object key order is irrelevant. List order is significant because optimization order can change a result. Booleans and integers remain distinct. Except for the certificate threshold, no algebraic equivalence of settings is inferred. Producers should canonicalize equivalent parameter expressions before saving records. Non-JSON or nonfinite settings and unknown descriptor keys raise `ValueError`. Additional configuration belongs inside `settings` so it participates in comparison.

Physical sizes and the temperatures or ranks selected by a shared optimization rule can differ between samples. Record the common size dependence or optimization rule in provenance, rather than substituting the selected result as the protocol identity. Use different IDs or settings when the rule or its implementation changes. A method using no trial states still supplies an explicit descriptor for that fact.

For example, this synthetic dataset illustrates the interface without asserting a physical certificate.

```python
from copy import deepcopy
from gapflow.forecast import forecast_seed_size

provenance = {
    "model_family": {
        "id": "spin_one_heisenberg_v1",
        "settings": {"spin": "1", "J": "1", "normalization": "S_dot_S",
                     "energy_shift": "0", "scope": "full_space"}
    },
    "geometry_family": {
        "id": "cycle_v1",
        "settings": {"shape_rule": ["n"], "size_unit": "sites",
                     "boundary": "periodic", "bonds": "positive_direction_multigraph"}
    },
    "temperature_protocol": {
        "id": "grid_minimum_v1",
        "settings": {"beta_grid": ["2", "4", "8"], "stop": "exhaust_grid"}
    },
    "trial_rank_protocol": {
        "id": "partial_ritz_v1",
        "settings": {"rank_rule": "min(6,dimension-1)", "tolerance": "1/1000000000"}
    },
    "certificate_criterion": {
        "id": "synthetic_scalar_test_v1",
        "settings": {"defect": "u", "comparison": "<=", "target": "unique_ground"},
        "threshold": "1/1000"
    }
}
records = [
    {"linear_size": n, "defect_upper": u, "evidence": "floating_estimate",
     "provenance": deepcopy(provenance)}
    for n, u in [(2, "1/10"), (4, "1/20"), (6, "1/40")]
]
result = forecast_seed_size(records, "1/1000")
assert result["sample_compatibility"]["status"] == "verified"
assert result["prediction"]["candidate_even_linear_size"] == 16
assert result["prediction_is_certified"] is False
```

### Compatibility and legacy data

Compatibility is checked across every input record before either accepting a tested scalar seed or fitting a trend. No record is silently discarded and no metadata is inferred from its size, evidence label or position in the input.

| `sample_compatibility.status` | Meaning | Effect |
| --- | --- | --- |
| `verified` | All five supplied descriptors are complete and equal, and their thresholds equal the requested threshold | Continue to scalar comparison and, if needed, the empirical fit |
| `unverified` | At least one descriptor or required member is absent or null, without a known conflict | Return `UNVERIFIED_SAMPLE_COMPATIBILITY` |
| `incompatible` | Known declarations disagree, or a recorded threshold differs from the requested threshold | Return `INCOMPATIBLE_SAMPLES` |

Known conflicts take precedence over missing information. The output identifies missing fields and conflicting fields with their physical sizes. Both blocked outcomes return `prediction=None` and `smallest_tested_sufficient_size=None`, even when an individual record is below threshold. The exact per-record arithmetic remains visible as `defect_at_or_below_threshold`. This boolean alone conveys neither a certified bound nor a compatible family. The returned samples preserve a copy of the supplied metadata, with thresholds normalized to rational strings.

Old records without provenance remain readable but cannot drive a size recommendation. Recover their definitions and settings from original input manifests before supplying them again. If those sources are unavailable, retain the `unverified` result. Copying the same invented ID onto old records does not establish comparability. Mixed datasets must be separated explicitly by the caller. There is no override that silently treats unknown provenance as verified.

### Scalar evidence and extrapolation

For compatible samples, a `certified_bound` at or below the threshold identifies a tested sufficient scalar seed. Comparisons use exact rational arithmetic, including equality and decimal differences below floating-point resolution. `smallest_tested_sufficient_size` is the smallest passing certified size in this supplied dataset. The input certification is caller supplied and is not independently reverified. Its model-to-seed proof and coverage bridge remain separate obligations.

With at least three distinct sizes and no tested certified success, the optional fit uses log(defect)=a+b*size to propose a next even size. Evidence labels may differ across otherwise compatible samples. A floating estimate below threshold cannot establish scalar sufficiency, and even a fit based entirely on certified bounds remains heuristic. No improving trend gives no finite crossing estimate. Too few data give an explicit missing-data result.

Compatibility has scope `declared_metadata_only`, with `source_artifacts_reverified=False`. It establishes agreement of the declarations rather than a new certificate. Every outcome retains `prediction_is_certified=False`, `input_bound_certification_reverified=False`, `minimality_proved=False`, `true_minimum_size=None`, and `uniform_gap_proved=False`. Neither compatibility nor a fitted crossing proves a minimum, failure at untested sizes, or physical gaplessness.

Run the forecast regressions from `gap_workflow` with `python -m unittest discover -s tests -p test_forecast.py -v`. They cover each source and protocol mismatch, incomplete legacy data, malformed metadata, evidence labels, early scalar success and exact rational boundaries. The 2026-10-14 [forecast audit](../audit/HOEFFDING_FORECAST_REVIEW.md) describes the earlier contract. Its metadata-free reproducer now returns `UNVERIFIED_SAMPLE_COMPATIBILITY`, while the boundary regression with complete provenance still excludes false scalar success.

## When more resources will not fix the chosen method

The connected ferromagnetic Ising diagnostic proves that near-one thermal purity cannot be reached because the ground space is two-dimensional. The global-width Hoeffding diagnostic separately excludes its original seed construction at specified couplings for every temperature and every larger seed. Both conclusions concern a particular criterion. They redirect the search to a different ground-space or tail bound instead of enlarging the same calculation.

The workflow distinguishes these mathematical obstructions from a timeout, a memory limit, an unsupported operator, an unverified spectral tail, and physical gaplessness. A failure of one route does not establish an impossibility theorem for all routes.
