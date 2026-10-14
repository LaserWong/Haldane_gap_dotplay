# Stage 1 independent final control review

Reviewed at 2026-10-14 19:47 UTC. No production source changes were made by this audit; additions are tests and audit artifacts.

## Verdict

No new certification soundness blocker found in the registered pinned-Ising and ferromagnetic-Heisenberg paths, `classical_seed.py`, `gapless.py`, `degenerate.py`, or `transfer_eligibility.py`. Their physical, finite-matrix, conditional, and structural scopes are appropriately distinct. Passing tests supplement the analytic review; they do not constitute exhaustive software verification.

## Pinned classical Ising

The normalization is H=J/2 sum(1-Z_i Z_j)+h/2 sum(1-Z_i), with Z eigenvalues +/-1, J>=0,h>0. A disagreeing edge costs J; a flipped spin costs h. Thus E>=h*k, exactly one configuration has zero energy, and the full gap is at least h. It need not equal h. Current metadata and CLI say “at least” and set physical_gap_is_claimed_exact false.

The counted trace envelope sums all binomial multiplicities: Z<=sum C(N,k)q^k=(1+q)^N. It is not a partial-spectrum truncation. With zero ground energy, each staircase numerator is at least one; all denominator volumes are no larger than V'=2^d V. Therefore P>=(1+q)^(-2V')>=1-2V'q. The common defect used by the code is conservative. The target exponent test is algebraically equivalent to the logarithmic bound with beta=log(1/q)/h.

Seed verification regenerates the entire canonical dictionary and compares it exactly. Tampering with h, purities, or analytic gap metadata was rejected independently. The CLI bounds max_power to 1..100, operates under its hard subprocess budget, and reports an exhausted search as insufficient evidence. It does not convert a finite search into nonexistence or minimality. Public low-level find_thermal_seed accepts any positive max_power, so callers outside the CLI must supply their own operational budget.

The classical transfer construction uses a symmetric bond table and half onsite weights, counts each periodic edge occurrence once, and retains doubled length-two bonds. The Pauli-to-spin parser conversion in the theory note, Jz=-2J and field_z=-h with scalar shift (sum_edges J+Nh)/2, is correct.

## True gapless Heisenberg control

The registered family is H=J sum(1/4-S_i dot S_(i+1)) with fixed J>0 and positive-direction periodic bonds. Each bond is (I-swap)/2. Positivity plus connected adjacent swaps proves that the complete ground space is Sym^L(C^2), dimension L+1, and that every finite L>=2 has a positive excitation gap above it.

The nonzero-momentum one-down-spin Fourier vector is orthogonal to the one symmetric state in its magnetization sector; all other ground vectors lie in other sectors. Thus it is orthogonal to the entire ground space. Its energy J(1-cos(2pi/L)) is positive and tends to zero. This supplies an upper bound on the first excitation and proves the lack of a positive uniform gap. It is not necessary to prove that this eigenvalue is the smallest excitation.

The L=2 doubled-bond convention gives excitation 2J, consistently with the formula. CLI claims explicitly distinguish uniform gap zero from finite-size gap positive. Unsupported couplings and extra finite solver/field parameters are rejected; no generic Hamiltonian is classified by numerical fitting or by degeneracy alone.

## Ground-space-aware temporal statements

For independently known exact ground multiplicity g and complete excited weights x_a in (0,1), the expressions for u and u(2beta) are correct. Since the largest Gibbs probability is 1/(g+S), gT<=g/(g+S), yielding S<=g*u/(1-u). Together with Q<=S^2 and u(2beta)<=2Q/g this proves the conservative 2g[u/(1-u)]^2 bound.

The implementation labels these as supplied spectral fixtures. It does not verify omitted spectrum or infer g from a numerical cluster. Empty weights are explicitly marked as no excited states. The theory does not substitute gT into the old spatial recurrence; it explains the changed exchange factors and transfer multiplicity obstruction. The separate Ising cycle all-size formula and gap J use the correct Sz=+/-1/2 normalization and even domain-wall counting, including L=2.

## Local structural witnesses

The realignment indexing maps -h_(a,c),(b,d) to R_(a,b),(c,d), so a nonnegative rational decomposition of R reconstructs -h=sum c*A tensor A. The code checks physical metric selfadjointness, symmetry and exact inertia of R, positive metric weights, and exact witness reconstruction. It uses the coefficient matrix rather than the metric-weighted energy form.

A successful witness remains LOCAL_IDENTICAL_FACTOR_WITNESS_VERIFIED with spatial_transfer_family_certified false. Missing onsite, family translation, boundary, directional, and template identity checks remain explicit obligations. A failed PSD route is inconclusive and can still be marked as eligible for a distinct classical diagonal route. The transfer theorem is an external analytic dependency; a local structural pass does not certify a uniform gap.

## Independent execution evidence

`audit/check_stage1_controls_independent.py` passed:

- 21 exact pinned-cycle configuration counts with J=0,1,3 and L=2..8.
- 280 exact rational temporal fixtures with g=1..7, including empty excitation lists.
- Six independently constructed full-space swap Hamiltonians, L=2..7, with magnon residual and overlap checked against every ground eigenvector. These particular checks use floating arithmetic and do not replace the analytic ground-space proof.
- 20 random rational identical-factor witnesses, independently reconstructed in original tensor indexing.
- Three altered canonical pinned-seed metadata cases, all rejected.

Record: `audit/stage1_controls_independent_results.json`.

`tests/test_workflow.py` now has 18 passing actual CLI subprocess tests. New cases cover pinned uniform lower bounds at strong J, exhausted and invalid power budgets, registered uniform gaplessness with positive finite gaps, and parameter/sector rejection. Log: `audit/cli_regression_results.txt`.
