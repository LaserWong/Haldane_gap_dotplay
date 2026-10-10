# Quantum-number scope clarification and dependency audit

Updated 2026-10-10 18:20 EDT (America/New_York) / 22:20 UTC.

## Exact findings

The five newly constructed vacuum/pair-orbit vectors are exactly spin-zero, cell-translation even and physical-reflection even. The reviewer directly verifies the same statements for every selected descendant and every saved full Hamiltonian image. These are exact integer/rational statements.

The inherited ψ and u vectors have exact M_z=0, but fail the exact translation, reflection and total-ladder tests. The nonzero raising/lowering supports are respectively 66,463 and 66,448 configurations. `inherited_quantum_diagnostic.json` gives explicit packed-state coefficient counterexamples, and `check_inherited_quantum.py` reproduces them from the immutable original packed files. This is not a floating tolerance judgment.

Therefore the entire combined 9D, 13D or 17D span must not be called an exact total-spin-zero, translation-even or reflection-even sector. These statements apply only to the five added bare directions and their pair-derived exact H-image descendants. Arbitrary physical trial vectors remain valid for all of the numerator Rayleigh, Gram-rank and whole-span LDL arguments reviewed here.

## Frozen producer prose requiring clarification

The pair-orbit producer README's “Exact sector and symmetry conventions” section correctly assigns the exact quantum numbers to each bare pair orbit and the vacuum, and correctly distinguishes their five-dimensional sector from the combined nine-dimensional span. The four-dimensional Krylov README does not assert exact symmetry for its inherited vectors.

The block producer README, “Construction,” ends its initial-span paragraph with the unqualified sentence “Translation and physical reflection eigenvalues are +1.” Read without a restricted antecedent, this could wrongly describe the complete nine-dimensional starting span or later combined spans. Its precise replacement is:

The five added bare vectors and their exact pair-derived Hamiltonian-image descendants have total spin zero, translation eigenvalue +1 and physical-reflection eigenvalue +1. The inherited rounded ψ/u vectors and the combined spans are not claimed to be exact symmetry sectors.

This erratum changes no frozen producer bytes. All exact numerical certificates remain valid. The old pair-orbit statement that no sufficient-path scan is warranted concerns only the old canonical-transport route; it must not discourage testing the separately proposed direct time-first window with the certified numerator.

## Accepted-proof dependency audit

The following accepted chain proof lineage was checked, together with the relevant exact checker code:

- `chain_frontier_review/FRONTIER_PROOF.md`, local full-space comparison and Temple enclosure
- `chain_frontier_review/independent_core.py`, `check_ground`
- `chain_temperature_review/REVIEW.md`, sections 2 and 3
- `joint_ratio_review/CHAIN_REVIEW.md`, sections 1 and 2
- `chain_low_band_review/COUNTED_BLOCK_THEOREM.md`, ground replacement and complete thermal count
- `chain_frontier_above_02_review/PROOF.md`, full-space ground and counted denominator
- `chain_frontier_rank195_review/PROOF.md`, actual M4 ground singlet and physical triplet trace lower bound
- `chain_m8_numerator_review/PROOF.md`, arbitrary-vector physical first moments and span exclusion

No accepted denominator or global-ground-identification argument in this lineage depends on these rounded M8 vectors being exact singlets or exact spatial-symmetry eigenvectors.

1. In the active temperature-first and joint-ratio chain certificates, M8 appears only through a normalized arbitrary physical vector's Rayleigh quotient. For every such vector, the variational/Jensen bound Z8(t)≥exp(−tρ8) holds. Exact trial symmetry, largest-seed uniqueness, ground isolation, residual and spectral-tail completeness are not required.
2. M4 denominator and ground identification use a physical local form bound with complete reference multiplicities over the full Hilbert space. They bound the full second eigenvalue, then combine rho<c with the complete residual to apply Temple. Neither the M4 trial nor the M8 numerator must be an exact singlet. The fact that the actual unique M4 ground is a singlet follows from Hamiltonian SU(2) invariance and uniqueness, not from a trial-vector symmetry label.
3. Earlier successful M8 Temple certificates use the same full-space reference-bin cutoff and full physical residual. The frontier proof explicitly disclaims spectral completeness inferred merely from a magnetization-zero trial space. The unsuccessful g=.2 historical largest-seed Temple record is not consumed by the accepted Rayleigh-only temperature-first route.
4. The counted denominator projectors and exact M4 spin-one triplet witness are independently constructed physical reference spaces/vectors. They do not borrow an exact-singlet assertion about the M8 rounded vectors. Thermal recurrence and final global-ground uniqueness use full physical traces and their inequalities, not a restriction to a numerator trial symmetry sector.

The new direct time-first window theorem is under separate review and is not certified or excluded here. `certified_numerator.json` remains a valid reusable numerator input for it.
