# Independent soundness review

Review time: 2026-10-14 19:28 UTC. Sources were being edited concurrently; findings refer to observed revisions and must be rechecked after fixes.

## Blocking findings

### 1. CLI loses decimal coefficient information before exact certification

Observed `gapflow/workflow.py` lines 72 and 129: plain `json.loads` converts decimal JSON numbers into binary floats. `Model._coefficient` then uses `Fraction(str(x))`, certifying the rounded decimal spelling rather than the original input. `Model.from_json` correctly uses Decimal, but the CLI does not call it.

Reproducer retained in `audit/decimal_rounding_input.json`:

- One spin 1/2, no edges, field `h=0.99999999999999999999`.
- Proposed ground energy `-1/2`, gap lower bound `1`.
- `python -m gapflow audit/decimal_rounding_input.json --output <fresh-directory>`.
- Observed `certified_finite_size` with exact full-space gap lower bound 1.
- Actual requested gap is `99999999999999999999/100000000000000000000 < 1`; actual ground energy is `-h/2`, not `-1/2`.

Original run retained under `audit/decimal_rounding_run`. Both exact and numerical backend comparisons agree on the wrong rounded model, so their agreement does not repair this provenance loss. Preserve decimal lexemes through input normalization, fingerprinting, serialization, and worker deserialization, or reject decimal numeric coefficients and require rational strings.

### 2. Empty excitation space mislabeled as an ordinary gap

Original `certify_gap([[0,0],[0,0]],0,100)` returned certified True with ground multiplicity equal to dimension. Author's concurrent fix observed: now returns False and `NO_EXCITED_SPACE`.

Remaining observed route: `spectral_gap_certificate([[0]],1)` returns certified True and gap lower 1. Require a nonempty excited space consistently across APIs, or define and label a separate explicit vacuous-gap convention. `certify_gap_from_vector` already requires dimension greater than one.

### 3. Stabilizer verifier accepts forged seed fields

Observed `gapflow/stabilizer.py`, `certify_target`: independently supplied seed dictionaries are trusted without reconstructing their physical thermal bound.

Reproducer:

    s = exact_thermal_seed([2])
    s['defect'] = '1/' + str(10**100)
    certify_target(s, 2)

Observed output: `EXACT_BOOTSTRAP_TARGET_VERIFIED`, `target_verified=True`, target gap 2, and simultaneously `full_family_gap_exact=1`.

Regenerate the canonical seed from shape/q/h and validate all derived fields, or make the function explicitly conditional scalar arithmetic with no physical verified status. Rejecting target > h is useful defense in depth, but alone does not validate general seed provenance.

## Positive checks

`audit/check_soundness_independent.py` was written separately from the implementation. It passed:

- 900 symmetric integer matrices: rational inertia counts vs NumPy eigenvalue sign counts.
- 331 applicable spectral-index tails: analytic rational upper bound vs full numerical spectrum.
- 350 positive-complement Schur cases: Schur inertia vs full rational inertia.
- Two nontrivial three-site XXZ + field + onsite-D models, uniform spin 1/2 and 1: exact builder vs independently assembled Kronecker spin operators.

Results are recorded in `audit/independent_check_results.json`. These are independent numerical diagnostics, not an independent exact proof implementation. Existing unit suite at the review point: 37 tests passed.

Reviewed mathematical details:

- Scalar and zero-diagonal 2x2 congruence pivots implement the correct inertia updates.
- Schur construction includes the full complement and requires strict complement positivity.
- Thermal-tail interlacing uses lambda_k(H) >= lambda_min(C), correct for a codimension-k compression, and its tail is explicitly spectral-index based rather than a projected heat trace.
- Ground upper bounds are Rayleigh bounds; no numerical Ritz value is promoted directly to a lower bound.
- Exact spin-1/2 and spin-1 exchange amplitudes are correct. Mixed/higher-spin transverse exchange fails closed; arbitrary spin is available numerically and diagonal exact models can work.
- Degenerate ground spaces with genuine excitations are handled by inertia and multiplicity counting.
- CLI final claims explicitly restrict selected-sector results to that sector and deny uniform-family conclusions.
- General bootstrap adapter calls its result conditional, records physical proof unverified, and does not assert a uniform gap from declarative proof strings.
- Resource output explicitly distinguishes physical sites, full Hilbert dimension, working-sector dimension, trial rank, and MPS bond dimension. Timing and memory figures are estimates. Tested sufficient seed size is not advertised as a proved minimum.

## Nonblocking limitations / integration advice

- Exact certificate and candidate artifacts should carry explicit model hash and sector identity themselves, not only depend on the enclosing run/input/checkpoint. Detached `certificate.json` currently states finite input matrix but can lose its sector context.
- CLI exact verification uses full working-matrix inertia. It is a small-matrix verifier, not yet a large-space partial-spectrum completeness proof. For larger dimensions the correct outcome remains candidate-only.
- A replay through the same inertia code is not independent exact verification. Current validation labels acknowledge this accurately.
- Resource estimates cannot establish a minimum physical seed size; no general model-to-geometric-bootstrap adapter currently closes that loop.

## Recheck at 19:29 UTC

- Stabilizer seed tampering now raises `ValueError: Seed metadata or bound mismatch: defect`. Parent implemented canonical regeneration and target <= h defense.
- Singleton `spectral_gap_certificate([[0]],1)` now returns `NO_EXCITED_SPACE`, `certified=False`, and no gap lower bound.
- Additional provenance check: `_spin2` converts through float, so `Decimal('0.50000000000000000001')` is accepted as spin 1/2. The spin validator should check exact half-integrality, without rounding an invalid spin into a supported one. This is an input-validation defect, distinct from the demonstrated incorrect coefficient gap certificate.

## Decimal and spin regression recheck at 19:30 UTC

The original false-certification input now returns `candidate_only`; `certificate.json` says `certified: false`. Its exact ground-energy proposal is rejected by inertia, as expected. Normalized `input.json` preserves field coefficient `"0.99999999999999999999"` exactly. Evidence is in `audit/decimal_rounding_fixed_run`.

`Model.from_dict` now rejects `Decimal('0.50000000000000000001')` as a non-half-integer. All original blocking findings are resolved in the revisions tested. An independent audit of the new generalized rational spin pencil is pending implementation.

## Generalized rational spin pencil audit at 19:31 UTC

New API `Model.exact_pencil` and generalized inertia/gap certifiers were checked independently after implementation.

`audit/check_pencil_independent.py` builds orthonormal spin operators using SymPy exact radicals and Kronecker products, without using the implementation's divided-power ladder formulas. It checks exactly, entry by entry, that `A_ij = sqrt(w_i*w_j) Hphysical_ij`.

Passed mixed/higher-spin cases `(1/2,1)`, `(3/2,2)`, `(2,2)`, and `(1/2,1,3/2)`, with XXZ exchange, field, and onsite anisotropy. Checks cover all four full spaces and every magnetization sector, 32 matrices total. Inertia also matches independent numerical physical spectra at a rational threshold.

Three Heisenberg pairs pass analytic angular-momentum ground energy, gap, and ground-multiplicity checks; proposed gaps above the actual gap fail. Nonpositive/mismatched/float metrics are rejected. Scalar pencils with no excited space fail certification consistently.

Record: `audit/pencil_independent_results.json`. The symbolic matrix-construction equality is exact; the eigenvalue-sign comparison is numerical. The implementation's exact inertia is still replayed rather than independently reimplemented.

All originally demonstrated false certificates are resolved by the tested revisions. This does not assert an exhaustive proof of software correctness or a general thermodynamic bootstrap implementation. CLI integration of the new pencil must retain the same decimal, sector, and finite-size scope safeguards.

## Independent end-to-end CLI regressions at 19:34 UTC

Added `tests/test_workflow.py`, invoking the actual `python -m gapflow` subprocess in isolated temporary directories. All 12 tests pass:

1. Full-space Heisenberg dimer exact gap and finite-only label.
2. Decimal lexeme negative repro remains uncertified.
3. Invalid near-half-integer decimal spin rejected.
4. Graph-state analytic uniform-family success, zero basis allocation.
5. Matching resume returns unchanged terminal result bytes.
6. Tampered certificate artifact rejected on resume without changing result bytes.
7. Tiny hard wall timeout returns resource limit, never gaplessness.
8. Dimension admission blocks candidate allocation.
9. Magnetization sector result is explicitly sector-only, using a field-shifted model whose physical ground lies outside that sector.
10. Mixed-spin generalized pencil certifies ground multiplicity two and gap 3/2.
11. Ferromagnetic Ising detector proves gap 1/2 and purity obstruction, without claiming gaplessness or a uniform-family bound.
12. A transverse spin-product model rejects a magnetization-sector request.

Evidence: `audit/cli_regression_results.txt`. Whole current suite: 69 tests passed, recorded in `audit/full_test_results.txt`. This closes the previously pending generalized-pencil CLI integration check.
