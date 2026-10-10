# Exact third-moment numerator: dependency and resource assessment

Updated 2026-10-10 15:27 EDT / 19:27 UTC.
**Assessment only. No new contraction or sparse support expansion launched.**

## Why a third moment helps

For a normalized original trial ψ, let ρ=<H'>, v=<H'²>−ρ² and r=(H'−ρ)ψ.
The two-vector variational space span{ψ,r} needs

    <r,H'r> = <H'³>−2ρ<H'²>+ρ³.

Thus exact H'³ gives the complete 2×2 Rayleigh pencil. It does not require H'⁴,
the residual of the filtered vector, or a new missing-state bound. The
resulting normalized even vector remains orthogonal to all old odd trials.

Current q-resolved filtering replaces R=<r,H'r>/v by an upper bound. At N=64:

| g | current certified R upper | exactly known <r,Qr>/v |
|---|---:|---:|
| .08 | 7.0604261673 | 5.9973117216 |
| .085 | 7.1290025825 | 5.9971998505 |
| .09 | 7.1978624369 | 5.9970845568 |
| .10 | 7.3363943872 | 5.9968459522 |

The second column includes interaction and cross-sector upper estimates. The
last column is not an upper bound on H'; replacing R by it would be invalid.
It merely locates where the current uncertainty lies. About 99.8% of residual
norm is in q=6, so its preserving interaction is the most relevant new term.

## What the existing data do and do not contain

The files named M0–M4 are moments of the smaller q≤2 base B. The current
11/29-dimensional ground family is span{B,H'B}, equivalently (B,L), with
L=A42 B independent of g. Its H'³ expectation generally needs the missing
B*H'⁵B term. Existing G/K/J and F/S/V/W do not directly supply that term.

Use H'=Q+tA with t=g/2. Let R4=A44 L and M6=A64 L. Existing contractions are

    F=L*L, S=L*A44 L, V=R4*R4, W=M6*M6.

For ψ=Bb+Lc, the q=4 and q=6 components of H'ψ are

    y4=L u+t R4 c,   u=4c+t b_pair,
    y6=t M6 c.

The missing preserving/cross contractions in <H'ψ,H'H'ψ> are

    X=R4*A44 R4,
    Y=R4*A46 M6,
    Z=M6*A66 M6.

They enter only through t³ c*(X+Y+Y*+Z)c. All other terms use the existing
q≤2 action and F/S/V/W. Consequently a reusable 14×14 combined geometric
matrix suffices at 8×8; three separate matrices are useful for testing but not
mathematically necessary. A fixed-vector scalar contraction is an alternative.
No q≥8 configurations are needed: only the expectation of H' within the
support of H'ψ is evaluated.

A cheaper intermediate option is to determine Z exactly and retain the
already certified bounds for the small q=4 and cross-sector pieces. This
would improve the variational numerator without claiming an exact H'³.

## Existing contraction architecture and exact translation reduction

`large_seed_moments/contract_geometry.cpp` already represents q=4 and q=6
singlets by 3 and 15 pair matchings, respectively. Their Gram contractions use
the exact loop factor 3. The preserving action is graph hopping plus
swap-minus-contraction on occupied edges. The q=6 preserving implementation
can use the same local rules as the already audited q=4 action.

The saved 8×8 geometry has:

- 635,376 four-site subsets, of which 478,176 are active
- 13,706,880 generated six-site candidates before deduplication
- 10,585,856 distinct six-site sets with potentially nonzero M6
- Audited baseline geometry runtime 5.46 s and peak child RSS about 106 MiB

For a translation-invariant scalar density f(S) on q-site subsets, transitivity
gives exactly

    sum_all_S f(S) = (N/q) sum_(S containing a fixed origin) f(S).

Proof: sum the indicator that the translated S contains the origin over all N
translations; each q-site S contributes exactly q. This uses every matching
coefficient and its metric contraction, not just an occupancy count.

At N=64 the q=6 target count therefore reduces exactly to 992,424, with
1,285,020 generated candidates; q=4 targets reduce to 39,711. The factors
N/q can be rational during accumulation, and divisibility must be checked at
the end. Translation of a pairing requires the correct induced permutation of
its labels.

## Resource estimate, not a benchmark

Streaming the fixed-origin masks needs roughly 10.3 MB before deduplication,
versus about 110 MB for the current unrestricted candidate vector. A cached
q=4 amplitude table and 14×14 accumulators should keep an implementation below
100–200 MiB, comfortably below 1 GiB, provided no full q=6 physical dictionary
is stored. Checked 128-bit or arbitrary-precision accumulators are required;
rounded 48-bit trial coefficients can make scalar totals exceed 128 bits.

Each q=6 target has at most 24 hopping neighbors and 15 occupied pair tests.
Evaluating their 15 matching coefficients suggests 10^8–10^9 local coefficient
operations after translation reduction. A plausible optimized C++ cost is tens
of seconds to several minutes on one CPU, but this has not been benchmarked.
It is not legitimate to extrapolate the old 5.46 s norm-only contraction
directly to the preserving-action contraction.

## Recommended gated implementation

1. Derive the new matching preserving action and normalization explicitly.
2. Test 2×2 and 4×2 against direct exact physical H'³ and the filtered Rayleigh
   quotient; verify the fixed-origin identity without a resource-heavy run.
3. Benchmark a 4×4 matching contraction and compare against an independent
   small physical-support expectation, retaining no q≥8 output.
4. Report measured operation rate, memory and projected 8×8 cost before a
   large run. Consider exact Z-only first, since q=6 dominates the residual.
5. Require an independent audit of new contractions before using any improved
   numerator in a published gap certificate.

The existing ordinary bilayer certificates and their frozen producers remain
unchanged. This assessment does not assert an attainable energy improvement
or that g=.09 will pass after such a contraction.
