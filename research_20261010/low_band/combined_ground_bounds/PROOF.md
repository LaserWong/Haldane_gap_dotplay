# Combining ground lower and variational upper endpoints

Updated 2026-10-10 15:00 EDT / 19:00 UTC.

## Scope and status

This directory is a scalar recombination of two new physical endpoint packages:
the full-ground inverse-moment pencil in `../ground_moment_pencil`, and the
implicit variational filter in `../../variational_numerator_filter`. The new
results remain **candidates pending independent review** until those packages
and the recombination have been accepted. Existing independently reviewed
records are not modified.

The model is the ordinary spin-1/2 square bilayer with unit AF rung coupling,
equal in-layer couplings g, and the periodic multiedge convention. The seed
patches have 16, 32, 64 rungs, hence 32, 64, 128 physical spins. Their full
Hilbert dimensions are 4^16, 4^32, 4^64. No full diagonalization is used.

## Independent roles of the endpoints

Write H' = H + 3N/4. The existing exact low-band proof identifies a unique
ground state and all 3N triplet modes, with all remaining ordered eigenvalues
bounded by the independently reviewed quadratic-boson reference. Its
oscillator multiplicities are retained without replacement by physical shell
counts.

The inverse-moment package gives a new lower endpoint l0 for the ground energy
of H'. The variational filter gives an upper bound u0 for the Rayleigh quotient
of one normalized implicit even singlet vector φ. These are independent facts:

    l0 ≤ λ0(H') ≤ <φ,H'φ> ≤ u0.

No residual or higher-moment bound for φ is asserted. The old triplet endpoints
remain unchanged. In particular, assigning u0 as the ground upper endpoint
does not assign it to an excited ordered eigenvalue or require the new vector
to be an approximate eigenvector.

For τ≥0, scalar Jensen and the spectral theorem give

    exp(−τu0) ≤ <φ,exp(−τH')φ>.

The existing normalized translated triplet trial vectors are odd under
triplet-number parity. They are mutually orthogonal after Fourier and spin
resolution, and orthogonal to the even φ. Therefore, adding their unchanged
Ritz exponential terms gives a valid trace lower bound. Alternatively, the
single term exp(−τu0) alone is valid, with no completeness or spectral cutoff
assumption at the largest numerator seed. Both variants are replayed for txy.

The ground trace upper term is exp(−τl0); all triplet and tail upper terms use
their old certified lower endpoints and multiplicities. Every accepted record
checks l0≤u0≤old Rayleigh upper exactly.

Although no new physical moments or sparse support are computed, φ generally
lies outside the original 11/29-dimensional ground trial subspace. It lies in
the implicit span{ψ,H'ψ}, of dimension at most two, and only one filtered ground
state is retained. This distinction is separate from both the full Hilbert
dimension and the retained 1+3N low-band count.

The optional filter consumes the original largest-seed G/K/J data and the
existing q-resolved geometry. Consequently this stronger variant does **not**
retain the strict largest-seed first-moment-only input property of
`../reduced_input`. Ground-only here refers to the number of numerator trial
terms, not to absence of original second-moment data in their construction.

## Correlated txy ratios

Let Z_N(τ) be the physical heat trace, with the geometry fixed by the rung
count. The initial correlated ratios are

    J1 = Z_64(2β) / Z_16(β)^8,
    J2 = Z_64(2β)^2 / Z_16(2β)^8,
    C0 = Z_64(2β) / Z_32(2β)^2.

Only the 64-rung seed is a numerator here. For the other two seeds, changing
the Rayleigh reference used to normalize the heat trace cancels algebraically
against its prefactor. Thus their filtered Rayleigh upper endpoints do not
directly improve these ratios when the physical lower endpoints are fixed.
Their improved pencil lower endpoints do improve the denominators. The
largest filtered upper endpoint improves the numerator directly.

The implementation preserves these correlated identities, rather than
multiplying independently bounded adjacent ratios. Every selected exact record
checks 0<J1,J2,C0≤1. The previously proved first-cycle inequalities and adjacent
axis transport then give the canonical triple at spatial base 8×8 and inverse
temperature 2β. No relabeling of thermal and spatial quantities is performed.

The `xty` and `xyt` comparisons reuse their already proved correlated identities
and transport. A largest-seed upper trace is needed in those orders; it is
retained there. Ground-only removal of largest odd trial terms is made only in
the txy numerator-only replay.

## All-size conclusion and limitations

The exact scalar recurrence and finite-window two-dimensional interpolation
are imported read-only from previously reviewed implementations. Each
successful record takes the minimum of its asymptotic recurrence gap, every
required finite-window gap, and an independently established L=2,…,7 bound.
For g≤.06 the stronger .06 short-size comparison is reused; for .06<g≤.10 the
uniform .10 quadratic comparison is reused. These are comparison-form
monotonicity statements, not assumptions about physical gap monotonicity.

Temperature selection uses only floating proposals on β=5,…,30 with step .05;
all selected endpoints, traces, transport, recurrence and windows are replayed
with directed rational arithmetic. Failure of this bounded proposal search
is not an all-temperature exclusion or a physical gaplessness claim.
