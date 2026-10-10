# Complete16D4x4 denominator residual at g=.105

2026-10-10 22:58 UTC / 18:58 America/New_York. Producer physical input pending independent review; no standalone all-size gap claim.

Use the already accepted16D third-moment basis B(6)+L(5)+U(5), adding five directions to the previously used11D4x4 B+L space. The exact rational vector is the saved outline_4x4.json candidate from the separately frozen optimized8x4 package. H'=Q+(g/2)A at g=21/200; the exact integer action is400Q+21A. The physical Hilbert space has32 spins and dimension2^32. This16D search is distinct from the49 retained denominator levels (one even ground plus48 odd modes).

prepare.py reconstructs periodic edges and pair orbits using translations, reflections and square-axis interchange in the same canonical minimum-pair ordering as the accepted basis. It first verifies its8x4 output against EVERY accepted edge/orbit identifier and then checks the4x4 pair-orbit Gram diagonals against the saved exact16D Gram. The produced4x4 geometry has16 rungs,32 unit-weight edges and5 pair orbits.

The unchanged accepted complete-residual engine processes all455 fixed-origin q4 supports and3003 q6 supports. It reconstructs the full q8 norm using CM plus the SIGNED hard-core commutator expectation. All cross terms, negative terms and nonzero q6 image components on M-zero supports are retained. The q0/q2 image is reconstructed independently from the full low rows of the exact first-Hamiltonian matrix. Orthogonal sector norms are summed before subtracting the exact mean squared. No projected-residual substitution and no q8 configuration enumeration are used.

The complete variance is .000022505420524742475...; exact rational and all sector norms are in physical_result.json. With the separately checked global-ground and even-sector cutoff conditions, Temple gives the ground lower -.14020845840321874.... This exceeds the chosen diagnostic target -.14045436638213465.... Target success alone is not a heat-trace or all-size certificate: all odd bands, omitted tails, scalar startup and integer-size coverage must still be checked.

The odd family atz=.1 remains unchanged. Its48 independent levels lie below the same q2 comparison cutoff. Together with the even trial mean below the q1 comparison, this identifies the unique even ground and justifies the sector Temple cutoff. The physical input changes only the denominator ground lower; any scalar use must retain the existing full counted spectral tail.

The exact same overflow checks and coefficient envelope as the optimized8x4 run apply. Coefficients are<=2^48, denominator400, A coefficient21. The conservative old2^56/denominator40 scalar envelope dominates these products. Arbitrary-precision sums handle norms and signed commutator terms.

Resources:CPU3,40CPU-second/100MiB cap. The contraction took .140793 seconds with2,176KiB peakRSS. Pure-Python exact assembly is separately capped at the same budget. Source, trial, geometry and predecessor seals are hash pinned; prior immutable files are unchanged. REPRODUCE.sh writes distinct check outputs.
