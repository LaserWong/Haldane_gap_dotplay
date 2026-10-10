# Improved spin-2 Heisenberg MPS witnesses

Model: H_N = sum_j S_j . S_(j+1), spin S=2, J=1, periodic boundary.

This directory provides improved *variational witnesses*. It does not prove a uniform gap or the purity bootstrap. Numerical optimization and finite-size certificates are deliberately separate.

## Numerical search

`opt_reduced.py` constructs a one-site SU(2)-invariant MPS from Clebsch--Gordan intertwiners and optimizes the infinite-chain energy with PyTorch LBFGS. The virtual representation is a direct sum of integer spins. Its invariant transfer fixed points lie in the commutant, of dimension sum_j multiplicity(j)^2. The reduced transfer has entries

T[(a,c),(b,d)] = p[a,b] p[c,d] (2 j_b+1)/(2 j_a+1),

where j_a=j_c and j_b=j_d. The optimizer obtains its left and right fixed points numerically. The two-site energy is contracted in the full virtual space. None of these eigensolver results is used as rigorous proof.

Initial D=48 energy was -4.760884453574416 in the infinite-chain contraction. Expanded candidates are in `improved84_state.npz`, `improved124_state.npz`, and `improved180_state.npz`. `_A.npy` gives normalized physical tensors in the orthonormal spin-z basis m=-2,...,2. `_history.json` records the numerical optimization. `improved84_gradient.json` compares eight autodiff gradients with central finite differences (largest discrepancy below 1.6e-9).

## Rigorous finite-size certificates

1. `build_exact_mps.py` converts reduced coefficients to an exactly specified integer tensor, preserving SU(2) covariance. The original periodic state is changed by rounding; the rounded tensor itself is the witness.
2. Its physical tensor is proportional to A_m = sqrt(binomial(4,m+2)) B_m, where each B_m is an integer matrix and the proportionality constant is irrelevant to a normalized state. A virtual gauge has already been incorporated into B. The builder forms the exact integer norm transfer and two-site energy insertion.
3. The builder constructs highest-weight blocks and checks their intertwining identities using exact integer arithmetic. The identities are checked, not inferred from numerical symmetry.
4. `verify_arb_mps.py` computes Tr(T^N) and Tr(T^(N-2) O), summed over all spin sectors with multiplicities 2J+1, using Arb ball arithmetic. Their ratio is the *energy per site*. A common exact power-of-two scaling of T and squared scaling of O cancel from this ratio.
5. The JSON certificate checks positive norm and energy < -a for each specified finite N. Consequently E_0(N)<-a N and Z_N(beta;a)>1 for every beta>0. This statement only covers the listed N; it is not an infinite-chain energy certificate or a spectral-gap certificate.

The D=84 integer witness certifies a=4.76105 at N=128,256,512. The D=124 integer witness certifies a=4.76121 at N=128,256,512 and additionally N=1024. The D=180 candidate is numerical only: its exact block build was deliberately stopped after J=0 because improved thermal moments, rather than this small additional energy improvement, remain the main bootstrap bottleneck. Certificate JSON records hashes of its exact blocks and integer tensor. All quoted decimal intervals are outward enclosures produced by Arb.

As a regression check, `old48_arb_certificate.json` reproduces the previous arbitrary-precision integer contractions for N=128,256,512 to all printed digits. This confirms the replacement of the contraction backend.

## Reproduction

Dependencies: Python 3, numpy, sympy, CPU PyTorch, python-flint (0.9.0 used for certification). The local `deps` directory is only an installation cache and should not be included in deliverables.

To reconstruct the certified blocks directly from the recorded integer tensor, avoiding any floating-point rounding:

    OPENBLAS_NUM_THREADS=1 python build_exact_mps.py --prefix improved84 --from-json
    OPENBLAS_NUM_THREADS=1 python verify_arb_mps.py --prefix improved84 --a 4.76105 --Ns 128 256 512 --prec 256

For the D=124 witness use prefix improved124 and a=4.76121. Files ending `_exact_build.log` give all exact covariance checks; `_arb.log` gives contraction progress. Do not infer a passed certificate from a partial log: inspect the final certificate JSON and all Boolean assertions.
