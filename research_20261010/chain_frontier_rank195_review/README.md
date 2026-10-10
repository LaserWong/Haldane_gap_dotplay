# Independent rank-195 frontier and numerator-span obstruction review

Updated 2026-10-10 17:57 EDT (America/New_York) / 21:57 UTC.

This package reviews the periodic spin-one alternating chain at g=.25, with unit strong exchange and all M weak links retained. It adds no positive all-size gap certificate. The separately sealed rank-67 review and its .21/.22/.225 certificates are preserved byte-for-byte.

## Results and their limits

1. Exact rank-195 small-seed physics: the M=4 reference is the complete weighted-energy space E<4. It contains one vacuum, twelve single triplets, fifty-four two-triplet states, 108 three-triplet states and all twenty single quintets. Q has dimension 6,366 and energy E≥4. Every full compression and residual matrix entry, local positivity and all 42 counted Schur endpoints are checked independently.
2. Fixed rank-195 recipe obstruction: for all temperatures the recipe cannot certify its mandatory first [8,16] window. This is stronger than the bounded floating scan's failure.
3. Denominator-independent obstruction: the same early-window recipe fails even with exact M=4 trace, for every one-term Rayleigh numerator drawn from the saved two-dimensional M=8 span. Exact spin-one trial vectors give a physical small-trace lower bound; an exact positive 2×2 form bounds every Rayleigh quotient in the saved largest-seed span from below.
4. Necessary numerator target: a one-term numerator for this same route must have ρ8<2ρ4+.0152≈−16.3544559234426, an improvement greater than .000426143856861 (exact threshold approximately .000426143856861833) over the saved value. This is necessary, not sufficient, and does not establish that such a state exists.

The obstruction is about computed certificate outputs. It does not upper-bound physical purities or prove absence of a physical gap. It does not exclude sufficiently improved numerator states outside the span, multiple certified numerator terms, other inequalities or orders, different seed geometry, or independent early-size bridges.

## Independent evidence

- Explicit spin-one physical matrices and orthogonal rational Clebsch–Gordan columns reconstruct all 195 reference columns.
- All 38,025 entries of each K, full J and full residual Gram are checked. The residual is constructed directly from leaked configurations and cross-checked with J−KG⁻¹K.
- Weak-action union 1,898; residual union 1,703, including 1,624 configurations containing quintets. Magnetic blocks have dimensions 4, 22, 44, 55, 44, 22, 4. These are dimer-basis support and linear-reference dimensions, not MPS bond dimensions.
- Fresh rational symmetric congruence verifies all 42 spectral threshold inertias without producer mathematical imports, isolated-Ritz-band assumptions, or floating degeneracy counts.
- Exact total-spin ladder identities verify the genuine triplet, with equal positive norms, equal full-action energies and orthogonality. The M_z=1 raising map has rank 22 in dimension 44, and the saved 22-dimensional kernel is independently checked.
- Sylvester's exact leading-minor/determinant criterion proves the saved two-dimensional largest-seed quotient bound for every real or complex coefficient vector. This is not a full-space M=8 ground lower bound.
- Three all-temperature claims each have 1,200 closed rational intervals covering β∈[0,12], plus an analytic tail for β≥12. Exponentials are replayed using separate 110-term Taylor enclosures and directed 384-bit arithmetic.
- The first-window formula and its exact domain are derived in PROOF.md. Its ideal output is I(P)=(sqrt(2P−1)+2P−1)/2 only when P>1/2; a positive gap requires P>(5−sqrt5)/4.

## Files

- PROOF.md: physical, counted-Schur, triplet, span and all-temperature arguments
- audit.py, physical_core.py, exact_inertia.py: independent exact physical verification
- audit_obstructions.py, scalar_core.py: independent all-temperature ceilings and required numerator target
- physical_premises.json, triplet_review.json, physical_endpoint_review.json: exact physical checks
- obstruction_review.json: three strictly scoped obstruction results
- adversarial_tests.py/json: deliberately corrupted physics, multiplet, span and interval inputs
- PROVENANCE.json and producer freeze copies: unchanged-source verification
- snapshot/: immutable producer bytes
- REPRODUCE.sh: clean sibling replay, never overwriting a frozen package

All computation uses CPU4 by default, one BLAS thread and a 1 GiB address-space cap. No full many-body spectrum is diagonalized. No original root, producer or GitHub files are changed. This is an executable exact-arithmetic mathematical certificate, not a proof-assistant formalization.

The three independently replayed maximal post-cycle product ceilings are .6118830239867779, .6693305924892161, and .6877367972629488, respectively. All are strictly below their exact rational comparison caps. Sixteen deliberately corrupted inputs were rejected. The obstruction replay used CPU4, took 149.21 wall seconds while sharing that same core with the spectral audit, and peaked at 20.16 MiB RSS.

All 42 exact physical endpoint checks passed. The initial physical replay took 446.23 wall seconds (including time sharing CPU4 with interval checks) and peaked at 44.03 MiB RSS. The verified rank-195 complement cutoff is 2.184511611252.

Presentation correction: the frozen producer prose uses “exceeding .000426143856862” for the necessary improvement. That decimal is rounded upward. The exact rational certificate remains valid; use the exact threshold in obstruction_review.json, the safe strict decimal >.000426143856861, or label .000426143856862 as approximate. DECIMAL_DISPLAY_CHECK.json verifies both rounding directions. Producer bytes remain unchanged.

Final status: accepted exact results with the decimal presentation correction above. Clean sibling reproduction passed all physics, triplet, span, interval and adversarial checks. Both producer and the completed rank67 review seals were rechecked unchanged after replay. See ACCEPTANCE.json.
