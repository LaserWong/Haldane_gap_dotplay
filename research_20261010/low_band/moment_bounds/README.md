# Direct moment bounds and sector-Temple certificates

Checkpoint: 2026-10-10 14:07 America/New_York / 18:07 UTC.

This directory is a separate successor to the immutable angle-based candidates in `../translation_band/refined/`. It changes no physical moment input.

## Result and verification status

For the ordinary spin-1/2 periodic square bilayer with unit rung coupling and equal antiferromagnetic straight in-layer couplings g, the new exact arithmetic candidates are:

| g | initial beta | gap lower bound | direct size scope |
|---|---:|---:|---|
| 3/100 | 277/20 | 0.282017228092 | every integer square side L >= 8 |
| 1/25 | 64/5 | 0.180632156388 | every integer square side L >= 8 |
| 1/20 | 249/20 | 0.104475599844 | every integer square side L >= 16 |

The complete underlying geometry, ground moments, translated-band moments, number-sector bins, and older angle-based trace certificates have passed the independent larger-seed audit. Both new analytical lemmas have also received an independent check. Independent arithmetic replay of these new Temple records and finite-size bridges is pending at this checkpoint. No all-L claim is made here until those checks are completed elsewhere.

The largest seed has N=64 rungs, 128 spin-1/2 sites, and full Hilbert dimension 4^64. Its retained complete low band has dimension 193. Its ground trial comes from 29 exact symmetry/Krylov vectors. Its triplet trial has 64 translation directions and exact spin multiplicity three. These are linear trial-space dimensions, not matrix-product-state bond dimensions.

## Exact proof of the new endpoint

The frozen number-sector bounds give lambda_(2+3N) >= a. The ground plus 3N triplet trial directions all have Ritz values below a, and are split into mutually orthogonal invariant momentum/spin/parity sectors. Hence exactly one eigenvalue in each represented rank-one sector is below a. No other sector can contain a further low eigenvalue. This external count is essential.

For one normalized sector trial with Rayleigh quotient theta<a and full residual squared r2, the unique eigenvalue in that sector obeys the Temple inequality

    theta - r2/(a-theta) <= lambda <= theta.

All moments include the complete leaked Hamiltonian image. Triplet theta and r2 are exact elements of Q(sqrt(2)). The endpoint is evaluated in that field and rounded downward using an integer-square-root enclosure. Ground moments are rational and contracted again from the saved full integer matrices and integer coefficient vector. Every new patch records the SHA-256 of each physical source.

The complete heat trace combines all retained individual eigenvalue intervals
with the unchanged ordered number-sector bins for every omitted state. Directed
dyadic exponential bounds and the canonical x,y,temperature correlated update
are unchanged from the independently checked pipeline. The first staircase has
n=m=8, reflecting the 4x4,8x4,8x8 seed family.

## General multilevel theorem

Let W have k independent columns, exact full moments G=W*W, A=W*HW and
B=(HW)*(HW), and assume lambda_(k+1)(H)>=a and A-aG negative definite. Set

    K=A-aG, S=B-2aA+a^2 G.

Then S is positive definite. The negative generalized eigenvalues mu_1<=...<=mu_k of (K,S) give lambda_i(H)>=a+1/mu_(k+1-i). A rational l<a is a certified lower endpoint for lambda_i whenever

    inertia_negative[B-(a+l)A+alG] >= k+1-i.

Proof: X=(H-a)W has full rank, and the Moore-Penrose inverse M=(H-a)^dagger has exactly k negative eigenvalues nu_j=1/(lambda_(k+1-j)-a). The identities X*X=S and X*MX=K hold even if H has eigenvalues exactly at a. The Ritz minimum principle gives nu_j<=mu_j<0. Taking reciprocals reverses the inequality, producing the claimed lower endpoints. The inertia test is the generalized eigenvalue count at 1/(l-a), after multiplication by the positive scalar a-l.

This theorem requires no residual norm bound, principal-angle estimate, or separately estimated complement compression. It still requires the external all-state count. Small residuals cannot supply that count.

## Files and replay

- `moment_endpoint.py`: arbitrary exact rational G/A/B moment-pencil acceptance.
- `validate_moment_endpoint.py`: 72 exact rational examples with known spectra, nonorthogonal trials, and cutoff equality, three exact direct-complement tests, and a counterexample showing why the external count cannot be omitted.
- `moment_validation.json`: all exact internal test outputs.
- `translated_temple.py`: new sector endpoints, whole-spectrum trace and replay.
- `translated_*_temple_low_band.json`: nine patch records.
- `temple_seed_g*.json`, `temple_seed_summary.json`: exact candidate records.

From the repository root, use single-thread BLAS and no bytecode writes:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python research_20261010/low_band/moment_bounds/validate_moment_endpoint.py
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python research_20261010/low_band/moment_bounds/translated_temple.py

The second command regenerates files in this directory. Copy the scripts and redirect outputs if preserving the frozen hashes. The recorded candidate run took 11.33 seconds under a 1.9 GB virtual-memory cap.
