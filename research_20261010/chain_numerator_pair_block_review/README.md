# Independent pair-orbit and block-numerator review

Updated 2026-10-10 18:21 EDT (America/New_York) / 22:21 UTC.

## Accepted physical results

The periodic alternating spin-one chain at g=.25 has independently verified numerator trial spaces of ranks 9,13,17. Their selected exact Rayleigh shifts δ=ρ8−2ρ4 are approximately:

- Rank 9: .015311537528561982
- Rank 13: .015308489680354413
- Rank 17: .015304451528169765

The rank 17 producer numerator_input.json is verified against the complete physical matrices and saved coefficient vector. Its exact norm, energy numerator, Rayleigh quotient, δ and source hash match. The reusable independent certificate is certified_numerator.json. It represents one numerator Rayleigh term, optimized in a 17-dimensional space, for 16 physical spins in full Hilbert dimension 43,046,721.

Every complete span has positive exact Gram and H−(2ρ4+.0152)G pivots. These all-span exclusions concern only the OLD canonical-transport early-window recipe. They do not exclude the separately proposed direct time-first window a²sqrt(2b−1), whose theorem and sufficient paths are under separate review. This package claims no positive all-size gap and no physical no-gap result.

## Complete new sector, with an important symmetry boundary

The five added bare directions form the complete translation-invariant singlet sector at weighted dimer energy E≤2: vacuum plus four unordered-pair singlet separation orbits. The 28 pairs partition into orbit lengths 8,8,8,4. The norms are 6561,69984,69984,69984,34992. All five directions and every pair-derived selected vector/full H image are exactly spin-zero, translation+1 and physical-reflection+1.

The inherited ψ/u vectors are only exactly M_z=0; they are NOT exact translation/reflection eigenvectors and are not annihilated by total raising/lowering. Hence the combined 9D/13D/17D spans are not wholly exact symmetry sectors. This does not affect the arbitrary-vector Rayleigh, rank or whole-span LDL proofs. SYMMETRY_SCOPE_ERRATUM.md narrows the ambiguous producer wording and audits the accepted-proof dependencies. No accepted M4 denominator, full-space ground identification or M8 Rayleigh numerator argument relies on these rounded M8 vectors being exact singlets.

## Exact verification

- All bare states, orbit completeness, norms and quantum numbers are independently reconstructed.
- Every full new H image is reconstructed without support or weighted-energy truncation. The first bare-image union has 1,961 configurations; the latest four images have supports 34,402; 100,867; 102,894; 68,400.
- All overlaps and energy cross terms with the sealed old 4D span and between new columns are checked. The accepted old 4×4 blocks remain unchanged.
- Every primitive normalization and sequential Gram-rank test is replayed. The vacuum image is dependent because A|vac>=−2304|vac>+36b1; four other images raise rank 9 to 13, and the next four raise it to 17.
- All rational coefficient quotients and complete-span target pivots pass, including complex coefficient vectors.
- Twelve corrupted inputs are rejected. Exact counterexamples document the inherited-vector symmetry limitations.
- Full physical replay took 18.19 CPU seconds and peaked at 297.15 MiB RSS, using CPU4, one BLAS thread and a 1 GiB address-space cap.

## Evidence and reproduction

PROOF.md contains the sector, physical-action, rank and scope arguments. exact_reviews.json holds complete rational checks; certified_numerator.json is the reusable rank 17 input. inherited_quantum_diagnostic.json and check_inherited_quantum.py give explicit exact symmetry counterexamples. SYMMETRY_SCOPE_ERRATUM.md explains why no existing accepted certificate is invalidated.

REPRODUCE.sh performs a clean temporary sibling replay, including the quantum-scope checks. PROVENANCE.json binds both producer freezes and all completed rank-67, rank-195 and 4D review seals. All producer and predecessor bytes remain unchanged. No root or GitHub files are changed. This is an executable exact-arithmetic certificate, not proof-assistant formalization.

Final acceptance: all exact physical, numerator, rank and old-target checks passed clean sibling reproduction. The explicit symmetry-scope erratum is part of the acceptance. The new direct time-first window is neither assessed nor excluded. Both producer and all predecessor seals were rechecked unchanged. See ACCEPTANCE.json.
