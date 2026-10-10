# Translation-compressed full-band certificates on larger tori

Updated 2026-10-10 13:59 America/New_York / 17:59 UTC.

The candidates in `refined/` use the sector-specific angle theorem below. They do not use the stronger direct Schur or inverse-operator lemmas in `NEW_MOMENT_LEMMAS.md`. All numerical candidates in this directory remain subject to independent review.

## Model, moments and one sparse column

Use the ordinary spin-1/2 square bilayer and normalization specified in `../PROOF.md`. The shifted Hamiltonian is H'=H+3N/4. Both straight in-layer couplings equal g≥0, with no crossed exchanges. The periodic positive-direction edge multiset retains all length-two multiplicities.

Let P_q project onto states with exactly q triplet rungs, and define

    C_+ = Σ_q P_{q+2} H' P_q.

The localized bare vector v_r has a triplet of magnetization +1 at rung r and singlets elsewhere. The trial column is

    w_r=(I−C_+/2)v_r.

`translated_band.py` clears its denominator by storing W_r=2d w_r, where d is the integer denominator of H'. Its exact integer image is dH'W_r. Every configuration in that image is retained, including q=5 configurations outside the trial support. No sparse cutoff is applied to the residual.

The q=1 component of w_r is exactly v_r. Thus its N translations are linearly independent regardless of the coupling. The one-column support is at most 1+3(2N−4)=6N−11 for a simple degree-four rung graph. The implementation obtains 85, 181 and 373 configurations for N=16,32,64. Their complete H' images have 3,185, 15,466 and 67,755 configurations.

The orthogonal rational dimer basis has labels 0=singlet, 1=triplet−, 2=triplet0 and 3=triplet+, with squared norms 2,1,2,1. The metric of a configuration is the product of its local squared norms. All contractions include that metric exactly.

## Exact spin multiplicity

H' and every P_q commute with total spin, so C_+ is an SU(2) scalar. Each w_r therefore has total spin 1 and magnetization +1. As a separate algebraic check, `verify_translation_small.py` applies total S+ exactly to the sparse column and verifies zero on all three sizes. The local raising coefficients in the rational basis are 1 for label 1→2 and 2 for label 2→3.

The maps S−/√2 from magnetization +1 to 0 and from 0 to −1 are isometries on the spin-1 representation. They commute with H' and spatial translations. Consequently the three spin copies have identical Gram, Hamiltonian and H'² moments. The translated band has full-space dimension 3N. This multiplicity is an exact representation-theoretic statement, not an inference from numerical degeneracy.

The ground trial is an exact spin singlet with even triplet parity. The translated triplet columns have odd triplet parity. Their cross Gram, Hamiltonian and H'² blocks vanish exactly.

## Translation moments and exact Fourier arithmetic

Translations act unitarily in the physical metric and commute with H'. Write

    G_rs=⟨w_r,w_s⟩,
    A_rs=⟨w_r,H'w_s⟩,
    B_rs=⟨H'w_r,H'w_s⟩.

All three matrices depend only on displacement s−r, so only the correlations of one sparse column are needed. Reflection symmetry and, for squares, coordinate exchange reduce the number of distinct displacement contractions further. The integer denominators are retained separately in the saved moment files.

Discrete Fourier characters simultaneously diagonalize the three translation matrices. For each momentum k, their scalar symbols G(k), A(k), B(k) satisfy

    G(k)>0,
    θ(k)=A(k)/G(k),
    r²(k)=B(k)/G(k)−θ(k)²≥0.

The formula for r²(k) is the full Ritz residual in the physical Hilbert space, since different momentum sectors are orthogonal and H' preserves momentum. Each represented momentum sector has one retained trial direction.

For side lengths dividing eight, the real Fourier symbols belong to Q(√2). The code evaluates them exactly as rational pairs a+b√2. Division uses the conjugate and comparisons use rational signs and squared magnitudes. Rational upper and lower endpoints use an integer-square-root enclosure of √2. Floating arithmetic only proposes an endpoint for the final Schur test.

On 4×4, `verify_translation_small.py` independently builds the general rectangular dimer-basis Hamiltonian map and all 16 translated columns. It checks every entry of the 16×16 G, A and B matrices against the correlation construction, for 768 exact equalities. This is stronger than checking only diagonal moments. The supporting file is `translation_crosschecks.json`.

## Number-sector bins without occupation enumeration

The local and Jacobi comparison from Section 6 of `../PROOF.md` remains unchanged. The only new ingredient is a safe upper bound on maximal occupied-edge count without enumerating 2^N subsets.

For a rung subset A with q vertices, let e(A) be its induced edge weight and let ∂A be its edge boundary. Degree four gives

    4q=2e(A)+|∂A|.

Let h=min(q,N−q). The periodic rectangular graph obeys

    |∂A|/2 ≥ min{ceil(2√h), nx, ny}.

It suffices to consider q≤N/2 because the boundary is unchanged by complementation. If A has no full row or column, every nonempty row and column is partial. If there are r such rows and c such columns, then q≤rc, and each partial cycle contributes at least two boundary edges. Hence |∂A|≥2(r+c)≥2ceil(2√q).

If A has a full row and no full column, every column is partial, giving at least twice the number of columns in boundary edges. The transposed case is identical.

If A has both a full row and a full column, no row or column is empty. Every point of the complement lies at an intersection of a partial row and partial column. Thus rc≥N−q≥N/2 and r+c≥√(2N)≥min(nx,ny). The boundary is again at least twice the smaller side. These arguments remain valid for length-two cycles when their parallel edges are retained.

Consequently

    e(A) ≤ 2q−min{ceil(2√h),nx,ny}.

For simple even-sided tori, bipartiteness supplies a second bound

    e(A)≤min{2q,floor(q²/4)}.

The identity

    e(A)=4q−2N+e(A complement)

also transfers this bound from the complementary size. The implementation takes the minimum of these proven upper bounds. Its records explicitly identify them as upper bounds, not exact occupancy maxima.

The resulting empty-edge upper bound is 2N−4q+e_upper(q). Using larger safe edge counts only enlarges the off-diagonal Jacobi norm bounds and can only weaken the final lower spectrum bins. Every candidate Jacobi endpoint is accepted by positive rational LDL pivots in both parity chains. The new count bounds were checked against all previously audited exact occupancy maxima on 2×2, 4×2 and 4×4, with no violations.

## Full-band counting and sector-specific complements

Let a₀, a₁ and a₂ be the certified ordered-bin bounds for the shifted Hamiltonian. They give

    λ₁≥a₀,
    λ₂≥a₁,
    λ_{2+3N}≥a₂.

The ground trial has Rayleigh quotient ρ₀<a₁. Therefore the full ground state is unique. Every triplet sector is orthogonal to it and has lower spectral bound a₁.

The N translated spin-1 trial directions and their three spin copies, together with the ground trial, all have Ritz values below a₂. The variational principle gives at least 1+3N eigenvalues below a₂. The global bin inequality allows at most that many. Hence these symmetry sectors account for the complete low band. In each represented momentum and spin component there is exactly one eigenvalue below a₂, and all unrepresented sectors have spectrum at least a₂.

Apply the residual-angle theorem from `../PROOF.md` separately to each rank-one symmetry sector. A triplet mode has squared angle at most

    s_k² ≤ r²(k)/(a₂−θ(k))².

Its orthogonal-complement compression is therefore bounded below by

    b_k = a₂−(a₂−a₁)s_k².

The ground sector instead uses

    b₀ = a₂−(a₂−a₀) r₀²/(a₂−ρ₀)².

The code substitutes rational upper bounds for r²(k) and θ(k), with the denominator positive. This safely increases s_k². It verifies every squared-angle bound is below one and takes b=min{b₀,min_k b_k}. Unrepresented sectors already have lower bound a₂≥b. It finally checks that b lies above every retained Ritz value.

For each mode, a proposed rational lower eigenvalue l is accepted by the exact algebraic sign test

    (b−l)(θ(k)−l)−r²(k) ≥ 0.

The ground uses the same scalar test with its exact rational Rayleigh quotient and residual. This is precisely the rank-one Schur-polynomial certificate proved earlier. No numerical completeness or floating sign test enters acceptance.

## Ground moments and exact heat traces

The block-Krylov ground sources come from `../../large_seed_moments/`. The pipeline contracts each saved integer G, K and J with its integer coefficient vector, including the stated Hamiltonian denominator. It checks exact agreement with the source Rayleigh quotient and full residual before use. The removed common factor 2^N cancels from these quotients and is not silently mixed with older unnormalized files. Source hashes are embedded in every final patch record.

The complete-band trace bounds use the same formula as Section 5 of `../PROOF.md`, with the new number-sector bins. `fast_exp.py` from the independent reviewer supplies a bounded-denominator directed enclosure of every exponential. It accounts for Taylor truncation, dyadic rounding, repeated squaring and reciprocation. This choice avoids unbounded denominator growth and does not replace rigorous exponential bounds with floating arithmetic.

The larger patch family is 4×4, 8×4 and 8×8. Correlated ratios use the same trace cancellation identities as before, but the first updated staircase has n=m=8, not 4. This size is passed explicitly to the exact scalar replay. The saved canonical successes are provisional pending independent review of this larger construction.
