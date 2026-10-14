# Complete the low-energy pair-orbit numerator block

Updated 2026-10-10 18:05 America/New_York (EDT) / 22:05 UTC.

## Result

The saved M8 numerator spaces do not exhaust the translation-invariant total-spin-zero sector of weighted dimer energy at most two. That sector has exactly five dimensions, comprising the vacuum and four two-triplet singlet separation orbits. All five directions are independent of the old four-dimensional Krylov span. Their union gives a nine-dimensional numerator-only trial space.

At g=1/4 its saved exact rational Rayleigh trial improves the original numerator by approximately 0.00031460632829984975, including approximately 0.000010929884105177272 beyond the four-dimensional trial. The remaining delta = rho8 - 2 rho4 is approximately 0.015311537528561982. Exact positive rational LDL pivots of H_trial - (2 rho4 + 19/1250) G_trial prove that **every nonzero vector in the full nine-dimensional space** has delta > 0.0152. Thus this whole space fails the previously independently reviewed necessary condition, even with an exact M4 denominator. No sufficient-path scan or further denominator expansion is warranted for this block.

This is a finite-trial-space obstruction for the specified one-term Rayleigh numerator and time-first transported-[8,16] recipe. It is not a lower bound on the full M8 ground energy, an all-trial-state impossibility, or evidence against a physical spectral gap. No all-size gap certificate is claimed here. The accepted discrete frontier remains g=0.225.

## Exact sector and symmetry conventions

There are eight spin-1 dimers on a periodic ring, so the physical Hilbert dimension is 9^8 = 43,046,721. The Hamiltonian is the unchanged alternating chain with strong intradimer coupling one and weak interdimer coupling g=1/4. A dimer's excitation energies above its singlet are 0, 1, 3 for total spins 0, 1, 2, with degeneracies 1, 3, 5. The quintet weight is three. This weighted excitation energy selects trial vectors. It is not assumed conserved by H.

Below or at weighted energy two, only the vacuum, single triplets, and two triplets occur. A single triplet has spin one, so contributes no total-spin-zero vector. Two spin-one triplets have a unique singlet for each unordered pair of occupied cells. The 28 unordered pairs form four translation orbits of lengths 8, 8, 8, 4, corresponding to separations 1, 2, 3, 4. The singlet is symmetric under exchanging its two spin-one factors, so the opposite-pair stabilizer creates no sign or extra direction. Together with the vacuum, the exact invariant-singlet dimension is 1+4=5.

Using the existing unnormalized rational dimer basis, the pair singlet coefficients on labels (1,3), (2,2), (3,1) are +1, -1, +1. Each orbit sums once over distinct unordered pairs. Cell translation rotates the eight labels. Physical reflection reverses the cell order and swaps the two spins within each dimer. Each triplet contributes a minus sign, each singlet or quintet a plus sign. Every bare pair-orbit vector and the vacuum has translation eigenvalue +1 and physical-reflection eigenvalue +1. Exact total raising and lowering actions both annihilate them, with Mz=0. No independent reflection-odd singlet direction is missing in this weighted-energy sector.

The saved original two-dimensional space plus the five bare vectors has exact Gram rank seven. The four-dimensional Krylov space plus these vectors has exact Gram rank nine. Thus the intersection with the five-dimensional bare sector is zero in both cases, even if their projections onto low weighted energy have overlapping amplitudes. The rank statement concerns full physical vectors, not projected coordinates.

## Contractions, resources, and verification

The ordered trial basis is psi, u, 144 H psi, 144^2 H^2 psi, vacuum, pair separations 1, 2, 3, 4. Here psi and u are exactly the saved vectors in the frozen four-dimensional package. Its full 4x4 Gram/H block is reused unchanged.

Only 85 configurations enter the five new bare vectors. Their complete scaled Hamiltonian images occupy 1,961 configurations in union, including all leakage. These images are saved explicitly. Streaming the previous large image files gives all necessary cross terms, via Hermiticity <b,Hv>=<Hb,v>. No large H^3 psi image is constructed, and no full residual or spectral assumption is used. A full residual is unnecessary for a numerator-only Rayleigh trial.

The construction used 1.70 CPU seconds and 50,268 KiB peak RSS on CPU 3, with BLAS one thread and hard 700 MiB/600 CPU-second limits. The separate exact verifier reconstructs the bare vectors, symmetry actions, full Hamiltonian actions, streamed overlaps, all Gram/H entries, rank proofs, rational quotient, and whole-space target exclusion without importing the producer script or using an eigensolver. This is producer replay. Independent review remains separate.

Floating-point diagonalization of only the conditioned 9x9 trial matrix proposes coefficients. Saved rational coefficients, the Rayleigh quotient, and every proof pivot are then evaluated exactly. No full-spectrum diagonalization is performed.

For precision, the original required improvement is exactly the saved rational rho_old - (2 rho4 + 19/1250), approximately 0.00042614385686183293. A rigorous strict finite-decimal necessary improvement is >0.000426143856861. The number 0.000426143856862 is rounded and must be labeled approximate.

## Files and possible extensions

- pair_extension.json: complete bare vectors/actions, necessary old-vector entries, exact Gram/H matrices, coefficients, quotients, and positive LDL certificates.
- build_pair_extension.py: bounded construction and coefficient proposal.
- verify.py and verification.json: exact producer verification.
- REPRODUCE.py and clean_reproduction.json: clean sibling replay.
- EXTERNAL_INPUT_SHA256.json and FROZEN_MANIFEST.json: immutable provenance and package seal.

A cheap next candidate, if authorized, is to rank-test the Hamiltonian images of these bare orbit vectors against the nine-dimensional space and add only independent images. Their support union is already only 1,961, so this avoids committing to another large Krylov image. No such extension has been launched here. A new candidate must cross the exact necessary target and then pass the actual sufficient scalar conditions. Crossing the necessary target alone would not certify a gap.
