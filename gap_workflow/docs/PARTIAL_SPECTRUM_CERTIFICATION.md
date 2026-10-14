# Finite-matrix partial-spectrum certificates

The engine in [gapflow/certify.py](../gapflow/certify.py) separates floating trial states from exact finite-matrix statements. Each certificate concerns its supplied real symmetric matrix or rational weighted pencil. A selected-sector certificate covers only that sector. An all-volume spin-model gap theorem requires additional arguments.

## Floating candidates

`partial_ritz_candidates(H, k)` uses the smallest-algebraic iterative SciPy eigensolver. Dense arrays, sparse matrices and matrix-free operators are supported. `ritz_candidates(H, Q)` orthonormalizes a supplied trial basis and diagonalizes its compression. Both return Ritz values and residual norms, explicitly marked as uncertified candidates.

A residual of zero does not exclude missing low states. For H = diag(-5, 0, 2, 3), the trial space spanned by the second and third coordinate vectors gives Ritz values 0 and 2 with zero residual. It omits the true ground at -5. The tests exercise this case and reject its naive thermal-tail claim.

## Exact arithmetic

Exact entry points accept integers, `Fraction` objects or rational strings. They reject floats. They do not silently rationalize the model builder's floating output. A rational model source must be supplied separately, or an independently justified exact change of basis must first produce the rational matrix. No interval floating arithmetic is implemented.

`inertia(H, threshold)` counts all eigenvalues strictly below, exactly at, and strictly above the threshold. Exact rational congruences eliminate scalar nonzero diagonal pivots. If all diagonals vanish, a nonzero off-diagonal entry supplies an invertible 2 by 2 pivot with one positive and one negative eigenvalue. A remaining zero block counts nullity. This handles singular matrices without numerical tolerances or full diagonalization.

`schur_certificate(H, trial_indices, threshold)` splits the coordinate trial block A, coupling B and complement C. It verifies C - threshold I is positive definite by exact inertia. It then computes

S = A - threshold I - B (C - threshold I)^(-1) B^T.

The full inertia is the inertia of S plus the positive dimension of C. This verifies spectral completeness even when trial eigenvalues alone do not. Exact complement inversion remains cubic in the complement dimension. The method is an auditable small-matrix validator, not a scalable substitute for structural complement estimates.

`certify_gap(H, ground_energy, gap_lower_bound)` verifies an exact ground energy, its multiplicity and the absence of eigenvalues between that energy and the requested gap threshold. Equality at the upper threshold is accepted. Ground degeneracy is reported explicitly. A matrix whose entire space is ground space returns `NO_EXCITED_SPACE`, never a positive excitation-gap certificate. `spectral_gap_certificate(H, threshold)` can instead use a coordinate Rayleigh upper bound on the ground and an exact count of one eigenvalue below the threshold. `certify_gap_from_vector(H, vector, threshold)` computes the exact rational Rayleigh quotient v^T H v / (v^T v) and combines it with a full-matrix count of exactly one eigenvalue below threshold. A nonzero rational vector need not be an eigenvector. Explicitly rounding a floating candidate to rational components is permitted outside this function, provided that provenance is recorded. The proof uses only the supplied rational vector and matrix. It also records the exact normalized residual squared. The Heisenberg dimer tests cover an exact singlet and a deliberately non-eigenvector rational approximation.

`verify_gap_certificate` replays the exact computation from the matrix. It is not a second independent arithmetic implementation.

## Thermal tails and residual coupling

Let n be the full input dimension and k the coordinate trial dimension. Let gamma be the exact Gershgorin lower bound for C. By min-max, the zero-based eigenvalue lambda_k(H) is at least gamma. This statement does not assume the trial states contain the ground eigenspace. A coordinate Rayleigh quotient gives E0 <= u = min diag(A). For beta > 0,

sum from j = k to n - 1 of exp[-beta(lambda_j - E0)] <= (n-k) exp[-beta(gamma-u)].

This is a spectral-index tail, not the projected trace Tr(Q_perp exp(-beta H)). If gamma-u is nonnegative, the engine bounds the exponential by the exact rational reciprocal of a finite positive Taylor polynomial for exp[beta(gamma-u)]. Thus a `target_met` result uses exact rational comparisons, not floating exponential evaluation. If gamma-u is negative, this implementation reports no useful rational tail bound.

The residual block coupling is retained separately. Put r2 = ||B||_F^2 and a = GershgorinLower(A). For every rational t > 0, Young's inequality gives

H >= diag((a-t) I_k, (gamma-r2/t) I_(n-k)).

The engine reports these two block energy bounds and their minimum as a global ground-energy lower bound. They imply the unshifted heat-trace bound

Tr exp(-beta H) <= k exp[-beta(a-t)] + (n-k) exp[-beta(gamma-r2/t)].

This symbolic consequence uses spectral monotonicity of the trace, not operator monotonicity of the exponential. The exact spectral-index tail above is stronger for its particular purpose and does not need a coupling penalty. Neither the Frobenius norm nor a small Ritz residual supplies the missing complement lower bound by itself.

## Sufficient dimension and budgets

`search_trial_dimension` tests increasing prefixes of a specified coordinate order. It returns the first dimension whose rigorous tail upper bound meets the target. This is a sufficient dimension and an upper bound on a possible minimum for the fixed criterion and representation. Earlier failures mean the tested bound failed, not that no better trial space or certificate exists.

The search limits full matrix dimension, maximum trial dimension and elapsed time. The default exact matrix limit is 64. Time is checked between trials, so a single rational arithmetic operation is not preempted. Fraction bit growth is not separately bounded. These limitations make the implementation suitable for small verification tasks only. Large physical matrices must remain numerical candidates until a justified structural tail certificate is supplied.

For diag(0, 1, 4, 8), beta = 2 and target = 1/100, the default coordinate order certifies k = 2. A budget capped at k = 1 reports no certificate. The test also verifies that changing the source matrix invalidates a previously sufficient exact gap certificate.

## Reproduction

Run from the workflow root.

    python -m unittest discover -s tests -p test_certify.py -v

The tests include exact singular and 2 by 2 pivot cases, 90 random integer matrices compared with independent floating eigenvalue counts, a Schur/full-inertia crosscheck, rational tail targets, Young coupling bounds, sparse iterative candidates, degenerate ground states and the omitted-low-state counterexample. The floating comparisons are numerical crosschecks. The rational algorithms are the certificate arithmetic.

## Rational generalized pencils for arbitrary spin

A rational weighted basis can avoid irrational normalized ladder coefficients. `Model.exact_pencil()` supplies a symmetric rational A and a positive rational diagonal metric W. Physical energies are the generalized eigenvalues A v = E W v, equivalently the spectrum of W^(-1/2) A W^(-1/2). Sylvester congruence therefore identifies the inertia of A - t W with the number of physical energies below, at and above t. No square roots are evaluated in this certificate arithmetic.

`pencil_inertia(A, Wdiag, threshold)` implements that exact count. `certify_pencil_gap(A, Wdiag, ground_energy, gap_lower_bound)` certifies the gap above the entire exact ground eigenspace. `certify_pencil_gap_from_vector(A, Wdiag, vector, threshold)` instead uses the exact generalized Rayleigh quotient v^T A v / (v^T W v) and the full inertia count. Positive metric entries, dimensions and exact rational input are checked. Scalar pencils A = e W return `NO_EXCITED_SPACE`.

The trial coordinates must match the weighted basis. If q is a numerical vector in the orthonormal physical basis, first form v = W^(-1/2) q numerically and explicitly round its components into rational trial data. The exact proof then recomputes everything from those rational components. The recorded residual squared is

(A v - u W v)^T W^(-1) (A v - u W v) / (v^T W v).

This equals the normalized physical residual squared, with u the generalized Rayleigh quotient. Directly substituting physical coordinates q for weighted coordinates v generally changes the trial state.

Tests verify invariance under a diagonal basis rescaling, invalid metrics and floating-input rejection. A mixed spin-1/2 and spin-1 Heisenberg dimer has exact ground energy -1 with multiplicity 2 and excited energy 1/2 with multiplicity 4. Its rational pencil certifies the finite gap 3/2 exactly. The current coordinate-tail API does not implement generalized thermal-tail search.

## Exhaustive symmetry blocks beyond the full-matrix dimension cap

`gapflow/sectors.py` supplies a full finite-Hilbert-space proof when every conserved total-Sz block fits the exact block budget, even if the full dimension does not. The model must preserve total Sz. Exact dynamic-programming counts enumerate every nonempty total_m2 sector and verify that their dimensions sum to the full Hilbert dimension. The engine constructs and processes their rational pencils sequentially. It does not diagonalize their spectra.

`certify_sectors_gap(model, ground_energy, gap_lower_bound, max_sector_dimension=128)` adds exact inertia counts at the proposed ground energy and gap threshold across all sectors. It supports a degenerate ground space and requires that an excited space actually exists. `certify_sectors_gap_from_vector(model, trial_sector, vector, threshold, max_sector_dimension=128)` computes a weighted rational Rayleigh upper bound in the named trial sector, then counts every sector at the threshold. Exactly one eigenvalue below the threshold and a smaller Rayleigh upper bound certify a unique full-space ground and the difference as a finite gap lower bound.

The result records every sector dimension, threshold and inertia count. It labels coverage complete only after every nonempty sector has been included. Preflight rejects a block exceeding the cap before any pencil is allocated. Optional elapsed-time checks occur between blocks. Hard CPU, wall-time and memory enforcement belong to the external process runner. A partial run is never labeled a full-space certificate.

The executed regression case is the spin-1/2 nearest-neighbor antiferromagnetic Heisenberg model on an open 2 by 2 by 2 cube with unit exchange. Its full dimension is 256, while the largest of its nine magnetization blocks has dimension 70. A floating candidate is prepared only in total_m2 = 0 and explicitly rounded to rational coordinates. Exact all-sector inertia at energy -4 finds exactly one lower state. The exact Rayleigh quotient then certifies a gap greater than 4/5. This proof does not construct the full 256 by 256 Hamiltonian or compute its full spectrum. It remains a result for that finite open cube, not an all-size three-dimensional gap theorem.

Run the sector regression tests from the workflow root.

    python -m unittest discover -s tests -p test_sectors.py -v
