# Extend the pair-orbit block by two Hamiltonian images

Updated 2026-10-10 18:09 America/New_York (EDT) / 22:09 UTC.

## Results and scope

Starting from the frozen nine-dimensional M8 numerator span, two exact block-image extensions give trial ranks 13 and 17 at g=1/4. The physical system remains eight spin-1 dimers, with Hilbert dimension 9^8 = 43,046,721.

| Span | Improvement over original numerator (approximate) | delta = rho8 - 2 rho4 (approximate) | Increment over preceding span |
|---|---:|---:|---:|
| Rank 13 | 0.0003176541765074191 | 0.015308489680354413 | 0.000003047848207569355 |
| Rank 17 | 0.0003216923286920675 | 0.015304451528169765 | 0.000004038152184648411 |

Each exact Gram matrix is positive definite. For each complete span, the exact rational matrix H_trial - (2 rho4 + 19/1250) G_trial is also positive definite. Thus every nonzero vector, including complex coefficient vectors, has delta > 0.0152. These are rigorous finite-span exclusions for the **previous canonical-transport early-window recipe** whose independently reviewed necessary target was delta < 0.0152. They are not lower bounds on the full physical ground energy.

A newly proposed direct time-first window bound a^2 sqrt(2b-1) can bypass that recipe's old window threshold. This package does **not** exclude that new route. The exact rank-17 numerator is retained for immediate reuse in its actual sufficient-path tests. No claim is made here about whether those new tests pass. No physical-gap impossibility or all-size success follows from the present trial-span calculations.

## Construction

The initial nine-dimensional span and its Hamiltonian conventions are documented in ../chain_numerator_pair_orbits_025. It contains the old four-dimensional Krylov span plus the full five-dimensional translation-invariant spin-zero sector at weighted dimer energy at most two. Translation and physical reflection eigenvalues are +1.

At the first extension, exact Hamiltonian images of those five bare vectors are rank-tested sequentially. The vacuum image is dependent; the four pair-orbit images are independent. The resulting trial rank is 13. At the second extension, all four images of those newly selected vectors are independent, giving rank 17. Each candidate vector is divided by the positive gcd of its integer coefficients without changing its span. Every candidate, dependence pivot, selected vector, and full next Hamiltonian image is saved.

The basis order is the original four vectors followed by the five bare directions and then the newly selected directions in block order. All new full images represent 144 H acting on the corresponding selected primitive vector. Their actions include every nonzero output configuration; quintet energy remains three. No weighted-energy truncation of H is made. No large H^3 psi image is formed.

Cross terms with the old four-dimensional span are contracted by streaming the frozen full vectors on the required support. Hermiticity permits <Hv,w>/144 to determine each new Hamiltonian row. All new pairwise Gram and Hamiltonian terms are evaluated exactly. The old exact blocks remain unchanged. The exact verifier checks both orientations rather than relying on forced symmetry.

Only the small conditioned trial matrix is diagonalized numerically to propose coefficients. The actual coefficients are rationalized with vector-dependent integer norm scales, and their norms and Rayleigh quotients are recomputed exactly. The Gram-rank and necessary-target proofs use rational elimination, not numerical Ritz brackets or spectral isolation assumptions. These are numerator-only trials, so no full residual or omitted-state spectral claim is required.

## Resource bounds and stopping

Both blocks ran on CPU3 with one BLAS thread and hard limits of 700 MiB and 600 CPU seconds. Rank13 construction took 2.36 CPU seconds and 71,344 KiB peak RSS. Rank17 construction took 7.58 CPU seconds and 215,900 KiB. All blocks are durable JSON checkpoints.

The newest full images have supports 34,402; 100,867; 102,894; and 68,400, totaling 306,563 entries before overlap removal. The two latest improvements are only roughly 3e-6 and 4e-6, while the old necessary-target deficit remains roughly 1.04e-4. Work stops at rank17 as authorized, before a larger memory-growing block. This is a practical bounded-search stop, not a theorem that further images cannot help. There is no need to spend more on the old route before testing the already available numerator against the new direct bridge.

## Reuse and verification

The compact numerator_input.json records its exact norm, energy numerator and Rayleigh quotient for reuse. The exact numerator for the best saved trial is also block_2.json:exact_rayleigh. Exact coefficients, full Gram/H, norms implicitly reconstructible from them, delta, and all target LDL pivots are present. block_1.json retains the nested rank13 result. next_frontier stores complete scaled actions and permits later moment/block reuse without recomputing them.

verify.py independently replays the producer's block selections, all new full actions, streamed physical contractions, complete Gram/H blocks, rational Rayleigh values and exact positive target pivots without importing block.py or using an eigensolver. This is producer verification, distinct from an external independent review. REPRODUCE.py rebuilds both blocks in a clean sibling directory and compares every mathematical field, excluding runtime/RSS.

EXTERNAL_INPUT_SHA256.json binds prior frozen inputs; FROZEN_MANIFEST.json seals this package. The old rank67, rank195, four-dimensional and nine-dimensional packages are unchanged. The exact threshold arithmetic uses 19/1250; the older displayed improvement 0.000426143856862 is approximate, while >0.000426143856861 is a safe strict decimal necessity for the old route.
