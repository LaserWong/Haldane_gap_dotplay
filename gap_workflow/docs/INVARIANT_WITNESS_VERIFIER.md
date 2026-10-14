# Exact invariant-witness verifier

The new standalone module `gapflow/invariant_witness.py` implements the sufficient criterion described in `theory/INVARIANT_SUBSPACE_MULTIPLICITY.md`. The verifier leaves the reviewed CLI and quantum-Ising proof pins unchanged. It is not yet wired into the CLI and does not discover witnesses.

## Interface

Call `verify_invariant_witness(A, W, V, T, polynomial_coefficients, lower, upper, threshold)`.

A is a rational symmetric n by n matrix. W is either a positive rational diagonal vector or a rational symmetric positive-definite n by n matrix. V is an exact rational n by k witness, T is its rational k by k restriction, and polynomial coefficients are listed from highest degree to constant. Floats are rejected for every mathematical input.

The verifier requires lower < upper < threshold and checks all of the following before returning a ground multiplicity or gap.

- Positive definiteness of W and of the Gram matrix VᵀWV
- Exact invariance AV = WVT
- Exact annihilation p(T) = 0
- A squarefree p and exactly one distinct root in the ground bracket
- A positive restricted cluster rank from exact small-pencil inertia
- Matching full-pencil inertia, with no lower state and no additional state below the threshold
- A nonempty spectral complement

A successful result has `certified=True`, `status=CERTIFIED_GROUND_MULTIPLICITY`, inferred `ground_multiplicity` and `gap_lower_bound=threshold-upper`. The result includes exact Gram and restricted matrices, inertia evidence, polynomial coefficients and check outcomes. Mathematical false witnesses return a failure status with null multiplicity and gap. Malformed inputs or preflight dimension, degree or bit-cap violations raise an exception.

The supplied polynomial need not be minimal. A regression test uses a valid nonminimal annihilator while mocking matrix characteristic-polynomial calls to fail. No full characteristic polynomial or floating eigensolve is used by this verifier.

## Budget and scope

Defaults cap full dimension at 64, witness dimension at 16, polynomial degree at 16 and each rational input numerator or denominator at 4096 bits. A default ten-second cooperative limit is checked between phases. It cannot interrupt an arithmetic or Sturm operation. Intermediate coefficient growth is not capped. An external process runner is still needed for hard wall-time and memory enforcement.

With sparse A and diagonal W, witness verification costs approximately O(nnz(A)k + nk² + dk³) rational operations, apart from polynomial-root counting and the mandatory full inertia. Dense W adds O(n²k) multiplication work. This implementation stores dense lists and uses a straightforward matrix multiplication routine, so its actual matrix work does not exploit sparse structure. Exact full inertia remains cubic in full dimension. The benefit is avoiding a full characteristic polynomial when an exact small witness is available, not eliminating completeness work.

The statements cover the complete supplied finite pencil only. They do not establish a thermodynamic gap. A rounded Ritz basis cannot serve as a valid witness unless the exact invariance equation independently holds.

## Executed checks

Run from the workflow root.

    python -m unittest discover -s tests -p test_invariant_witness.py -v

The proper-subspace example uses two rational 2 by 2 blocks with eigenvalues ±sqrt(2), plus two higher scalar blocks. A four-dimensional witness inside a six-dimensional pencil infers ground multiplicity two and certifies gap at least two. Rejection cases include a splitting of 1/100000000, a witness leakage of 1/1000000000000, an omitted lower state, wrong and nonsquarefree polynomials, an indefinite metric, rank deficiency, floats and exhausted budgets. A dense positive metric and a nonminimal annihilator are also checked.
