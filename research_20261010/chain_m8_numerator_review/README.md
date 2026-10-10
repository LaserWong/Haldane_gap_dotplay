# Independent M8 numerator Krylov review

Updated 2026-10-10 18:07 EDT (America/New_York) / 22:07 UTC.

## Accepted result

At g=.25, the four-dimensional span containing both old M8 trial directions and Hψ,H²ψ is a valid, independently reconstructed physical trial space. Its selected rational Rayleigh vector improves the previous quotient by approximately .0003036764441946725. The remaining shift δ=ρ8−2ρ4 is approximately .01532246741266716.

Exact positive Gram pivots prove rank four. Exact positive pivots of H_trial−λG_trial, with λ=2ρ4+.0152, show that every nonzero real or complex coefficient vector in this entire span lies above the necessary numerator target. Reoptimizing its coefficients cannot fix that failure. The independently sealed all-temperature obstruction therefore applies to this space for the specified one-term Rayleigh/time-first/transported-[8,16] recipe, even with exact M4 trace.

This is a scoped exclusion, not a positive .25 gap certificate, a lower bound on the full M8 ground energy, or an exclusion of all numerator states. Different directions, multiple justified numerator terms, other inequalities/orders/geometries, and independent early bridges remain outside the claim. Separately evolving pair-orbit extensions were not read as acceptance inputs.

## What was independently verified

- Original ψ and the additional old direction are reconstructed from the two sealed original NPZ vectors and their exact integer coefficients.
- The physical spin-one kernel is rebuilt from explicit Clebsch–Gordan columns. Integer scale 144 clears the g=.25 Hamiltonian. All eight weak periodic links and complete strong energies are retained.
- Every coefficient of all three complete images matches: 144Hψ has 243,475 configurations; 144²H²ψ has 935,927; 144Hu has 243,438.
- Norms and physical moments through order five are independently contracted. The highest energy contraction enumerates 60,872,321 directed weak transitions. The auxiliary old-direction contractions also match.
- All 16 Gram and 16 Hamiltonian entries of the four-dimensional space, the saved rational Rayleigh value, positive norm and complete-span exclusion pivots match exactly. The two- and three-dimensional nested trial claims also replay.
- All amplitudes and contraction sums use Python arbitrary-precision integers, not fixed-width NumPy arithmetic. Images require up to 107 bits; the largest saved moment requires 237 bits. Packed-state and small local-integer bounds are checked separately.
- Twelve deliberately corrupted inputs are rejected, including missing action tails, duplicate states, altered moments, false rank and an unsafe raised threshold.

The largest physical seed still has 16 spin-one sites and full dimension 43,046,721. Its retained thermal numerator is one Rayleigh term, optimized in a four-dimensional linear space. Configuration support, linear dimension and MPS bond dimension are distinct. No full H³ψ vector, filtered residual, largest-seed omitted-state tail or physical low-band isolation is inferred. A first-moment contraction needs only bra-supported matrix elements; that fact does not remove any nonzero coefficient from the two saved full images.

## Evidence and reproduction

PROOF.md gives the exact model, full-action and contraction argument, span inclusion, overflow controls and scoped all-temperature implication. SUMMARY.json, independent_moments.json, four_span_review.json and nested_span_review.json hold exact results. overflow_and_structure.json and adversarial_tests.json document structural and negative checks. PROVENANCE.json verifies producer inputs and both completed rank-67/rank-195 review seals.

Run REPRODUCE.sh from any directory for a clean temporary sibling replay; it preserves the frozen originals. CPU4, one BLAS thread and a 1 GiB address-space limit are used. The initial full physical replay took 104.69 CPU seconds and peaked at 325.46 MiB RSS. No producer mathematical module or compiled binary is used for acceptance.

The producer manifest is cb2e5e34bf4f4cfbadcb2473109fd2f17f86ae46ae83366230865084932173d3. This review changes no root, producer, previous review or GitHub state. It is an executable exact-arithmetic mathematical certificate, not a proof-assistant formalization.

Final acceptance: clean sibling reproduction passed every exact physical, nested-trial, structural and adversarial check. Producer, rank-67 and rank-195 seals were rechecked unchanged after replay. See ACCEPTANCE.json.
