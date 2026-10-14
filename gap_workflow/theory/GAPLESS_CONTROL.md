# True gapless-family control: ferromagnetic Heisenberg ring

## Exact statement and conventions

For each integer L ≥ 2 and fixed J > 0, take spin 1/2 at each site and

H_L = J Σ_{i=0}^{L−1} (1/4 − S_i · S_{i+1}), indices modulo L.

Here ℏ=1 and S²=3/4. The sum counts positive-direction bonds. In particular,
L=2 has two copies of the same undirected bond. For L≥3 it is the usual ring.
A simple graph with only one bond at L=2 instead has gap J and is NOT the
L=2 convention used in the formula below. `ferromagnetic_cycle` uses the
existing model builder with exchange coefficient −J. Its energies differ
from H_L by the constant −JL/4; excitation gaps are unchanged.

Let Δ_L be the smallest eigenvalue strictly above the ENTIRE zero-energy
ground eigenspace. The theorem is

0 < Δ_L ≤ J[1−cos(2π/L)] ≤ 2π²J/L², for every L ≥ 2.

Consequently Δ_L → 0 and inf_{L≥2} Δ_L = 0. This is a genuine absence of a
positive size-independent excitation gap above the full ground space. It is
not merely the vanishing difference between two degenerate ground levels.
There is no assertion that any fixed finite ring has zero excitation gap.

## Proof of the complete ground space

For two spin-half sites, the swap operator P_ij satisfies
P_ij = 2 S_i·S_j + 1/2. Thus the bond term is

1/4 − S_i·S_j = (1−P_ij)/2,

the orthogonal projector onto the two-site singlet. Every term is positive
semidefinite. A vector has zero total energy if and only if each bond
projector annihilates it: the expectation of each positive term must vanish.
Equivalently it is invariant under each adjacent swap. The ring is connected,
and its adjacent swaps generate all site permutations, so the common kernel
is exactly the completely symmetric spin subspace Sym^L(C²). Its dimension
is L+1, with one normalized equal-weight state in each magnetization sector.
This argument also holds for the doubled L=2 edge. The kernel is proper
(for example a singlet has positive energy). In finite dimension the
nonzero spectrum of this positive operator has a strictly positive minimum.
This establishes Δ_L > 0 without a numerical tolerance.

## Explicit normalized excitation and orthogonality

Let |x⟩ denote the product vector with one down spin at site x and all other
spins up. These L vectors are orthonormal. Set q=2π/L and

|ψ_q⟩ = L^(−1/2) Σ_{x=0}^{L−1} exp(iqx)|x⟩.

Its norm is exactly 1. This state has total magnetization L/2−1. All ground
states in other magnetization sectors are orthogonal to it. The unique
symmetric ground state in its own magnetization sector is
|ψ_0⟩ = L^(−1/2) Σ_x |x⟩. Their overlap is L^(−1) Σ_x exp(iqx)=0,
because exp(iq) is a nontrivial Lth root of unity for every L≥2. Hence
|ψ_q⟩ is orthogonal to the ENTIRE ground space, not just the polarized vacuum.

On this one-magnon subspace the projector sum gives

H_L|x⟩ = J|x⟩ − (J/2)(|x−1⟩+|x+1⟩).

At L=2 the two neighboring kets coincide, but the two bond occurrences
supply their two contributions, so the same expression remains correct.
Fourier summation now gives the exact excited eigenvalue

H_L|ψ_q⟩ = J(1−cos q)|ψ_q⟩.

It is strictly positive at q=2π/L. By the definition of the first excitation,
Δ_L is at most this eigenvalue. Finally 1−cos t = 2 sin²(t/2) ≤ t²/2
for real t (using |sin u|≤|u|). Taking t=2π/L proves the claimed bound.
The upper bound alone suffices to prove gaplessness; no all-size equality
between Δ_L and the magnon energy is needed or claimed by this proof.

## Executable diagnostic and finite numerical cross-check

`gapflow.gapless.diagnose_gapless_family()` recognizes only the explicitly
registered `ferromagnetic_spin_half_heisenberg_cycle` family. Its positive
rational J input specifies the model, rather than proposing a numerical
fit. A supported result has status `CERTIFIED_GAPLESS_FAMILY`, grounded in
the analytic proof above. Invalid inputs have no physical conclusion.
This is a family-specific theorem adapter, not a general gaplessness algorithm.

`numerical_control_check(L)` is a separate bounded floating-point sanity
check for 2≤L≤10, using the existing spin-model Hamiltonian builder. It
constructs and diagonalizes EVERY total-Sz block, so coverage sums to 2^L,
while the largest block is only 252. It checks the ground multiplicity and
first positive eigenvalue, the normalized magnon eigenvector residual,
and overlap with the symmetric state. Energies are normalized by J, so
extremely large or small rational J does not corrupt numerical tolerances.
The tests cover L=3,...,10 plus the L=2 doubled-bond edge case.

Run:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python -m unittest discover -s tests -p test_gapless.py -v

All five tests passed on 2026-10-14. The observed equality of the numerical
finite-size gap and magnon energy is a useful cross-check, not the all-size
proof. No floating-point quantity enters the analytic certificate.

## Distinct diagnostic meanings

- `CERTIFIED_GAPLESS_FAMILY`: an explicit orthogonal excitation proves a
  vanishing upper bound on the physical excitation gap.
- Method/criterion obstruction: a particular sufficient criterion cannot
  succeed, even when the physical model may have a positive uniform gap.
- Resource failure: the requested computation did not fit its budget.
- Inconclusive certification: no theorem or complete spectral bound was obtained.

Neither a failed purity test, growing ground-space degeneracy, finite-size
numerical extrapolation, nor a failed computation alone is a physical
gaplessness proof. This ring supplies the separate true-gapless control.
