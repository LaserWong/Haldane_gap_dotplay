# Independent audit: fully frustrated bilayer with unequal straight/crossed bonds

Updated: 2026-10-10 13:20 EDT / 17:20 UTC.

## Certified result and precise model

On a periodic square of integer side L >= 2, place two spin-1/2 sites on each rung. The rung exchange is 1. Every positive-direction nearest-rung adjacency carries two straight exchanges J + epsilon and two crossed exchanges J. Here J = 3/10 and epsilon = 1/200. Periodic directions of length 2 retain both adjacency terms; they are not deduplicated.

For this model the finite-volume ground state is unique and

**Delta_L >= 0.038983227177 for every integer L >= 2.**

The exact bound before decimal truncation is

13265304814131434363258744511923058681 / 340282366920938463463374607431768211456.

This is an independently audited sufficient bound at the specified epsilon, not the physical gap or a maximal coupling threshold. It is a genuinely two-dimensional square-volume result. It does not assert an arbitrary-aspect-ratio rectangular theorem.

The candidate is `low_energy/ff_seed_J3d10_eps1d200_depth0.json`; no baseline file was modified. Its original Hamiltonian includes the rung singlet energy E00 = -3N/4. Below, shifting by +3N/4 is used only to simplify the proof and never changes a gap.

## 1. Multigraph and weighted-star inequality

Let P_i project onto the triplet of rung i, T_i = S_i,0 + S_i,1, and Q = sum_i P_i. The shifted fully frustrated reference is

H_FF = Q + J sum_{i<j} w_ij T_i dot T_j.

The integer weight w_ij counts positive-direction periodic adjacencies with endpoints i,j. For every rung the weighted degree is 4, and sum_{i<j} w_ij = 2N, including the period-2 case.

For a triplet central spin and k occupied triplet neighbours, angular-momentum addition gives

T_i dot (sum_{j=1}^k T_j) >= -(k+1) I,  k >= 1.

Indeed the neighbour total spin S is at most k; the minimum scalar product is -(S+1) for S >= 1 and zero for S = 0. For nonnegative weights c_j, decompose them into nested level sets. Integrating the preceding unweighted inequality over the level parameter gives

T_i dot (sum_j c_j T_j) >= -(sum_j c_j + max_j c_j) I.

The right-hand side is zero for an empty neighbourhood. This argument covers unequal weights and parallel edges after their weights are combined.

Fix an occupied rung set A. Let E(A) be its total active edge weight, and m_i(A) the maximal active incident weight (zero if none). Summing the star inequalities counts each edge twice, hence

H_FF restricted to A >= f(A) I,

f(A) = |A| - J [E(A) + (1/2) sum_i m_i(A)].

This is an operator lower bound, not an assertion that all spins in A have energy f(A). Each occupancy block has exact rank 3^|A|. The independent audit enumerates all 2^N occupied subsets and verifies, separately for every q, that their total rank is binom(N,q) 3^q. The full rank is 4^N. There are 6, 28 and 115 distinct (q,f) bins for the 2x2, 4x2 and 4x4 seeds, respectively.

## 2. Local perturbation comparison and complete ordered spectrum

Write the straight-only perturbation as epsilon V, with

V = sum_{i<j} w_ij (S_i,0 dot S_j,0 + S_i,1 dot S_j,1).

For each seed, its stored rational a,b satisfy the exact 16-dimensional local inequality

epsilon (S_i,0 dot S_j,0 + S_i,1 dot S_j,1) + a(P_i+P_j) + b I > 0.

The audit reconstructs these matrices directly in the four-physical-spin basis and performs rational LDL elimination. All 16 pivots are strictly positive. The stored choices are:

- 2x2 and 4x2: a = 0, b = 3750000001 / 500000000000
- 4x4: a = 1290617 / 125000000, b = 1118196753 / 1000000000000

Summation over the weighted graph gives

H_epsilon >= D_a - B I,  B = 2N b,

where D_a is scalar f(A)-4a|A| in occupancy block A. The vacuum is the unique lowest block of D_a: its value is zero and every nonempty block is strictly positive, checked by exact enumeration. Min-max therefore bounds every ordered physical eigenvalue by the equally ordered eigenvalue of D_a-B. Although the perturbation no longer conserves occupancy, this ordered-spectrum implication remains valid.

In particular, after restoring E00, the second eigenvalue is bounded below by

alpha = E00 + min_{A nonempty}[f(A)-4a|A|] - B.

Every omitted eigenvalue is counted by the nonvacuum bins with total multiplicity 4^N - 1. No assumption that the perturbed eigenvectors stay in a fixed occupancy sector is made.

## 3. Exact complete residuals and unique-ground-state intervals

The independent verifier reconstructs rational, unnormalised rung vectors directly from physical spins, then applies every rung and inter-rung exchange to every trial basis vector. The sparse rectangular map includes every output state, including states outside the trial space. Exact integer arithmetic gives Rayleigh quotient rho and full residual squared r^2.

The saved and independently reconstructed values agree exactly, as do all reached dimensions and nonzero counts. Because rho < alpha, the second-eigenvalue bound proves uniqueness of the lowest state and gives the Temple enclosure

rho - r^2/(alpha-rho) <= E_ground <= rho.

The three geometries have:

- 2x2: 8 physical spins, full dimension 256, trial dimension 23, reached dimension 58
- 4x2: 16 physical spins, full dimension 65,536, trial dimension 93, reached dimension 1,301
- 4x4: 32 physical spins, full dimension 4,294,967,296, trial dimension 377, reached dimension 21,345

Only one Ritz vector is retained per geometry. The trial dimension counts its linear supporting space; it is not an MPS bond dimension. Independent expansion into the complete physical-spin basis also reproduces the Rayleigh quotient and full residual exactly for 2x2 and 4x2. The 4x4 audit uses the exact full-reached sparse action and does not diagonalize the 2^32 physical Hilbert space.

## 4. Thermal input and correlated three-purity recursion

Let l <= E_ground <= u be the exact ground interval. The complete ordered-bin result yields the upper bound

exp(beta u) Z(beta) <= exp[beta(u-l)]
  + sum_{nonvacuum bins (q,f)} multiplicity * exp[-beta(E00+f-4aq-B-u)].

Call this upper bound q_N(beta). The lower partition bound Z(beta) >= exp(-beta u) is variational. Both bounds account for the whole Hilbert space.

For the three geometries, abbreviate their upper energies U22,U42,U44 and normalized partition upper bounds q22,q42,q44. Exact cancellation of common heat traces before interval evaluation gives

J1 >= exp[-beta(2U44-8U22)] / q22^8,
J2 >= exp[-beta(4U44-8U42)] / q42^8,
C  >= 1/q44^2.

The first correlated update is A1 = G(J1), B1 = G(J2 A1), C1 = G(C^4 A1^2 B1), with G(x)=1-(1-x)^2/(2x^2). Thereafter the sequential three-purity recursion applies. All actual lower endpoints are rounded down to 128-bit dyadics.

The audit uses an independent exponential enclosure: 56 Taylor terms, argument reduction to at most 1/4, rigorous geometric remainder, and outward 192-bit rounding. It proves that every stored heat input is below this independent lower enclosure. It then exactly reconstructs all 128-bit recurrence steps. For the final logarithmic bound it checks exp(beta_final * gap) < 1/(32u_defect), independently of the producer's logarithm implementation.

At initial beta = 32 the accepted state has n = m = 8, beta_final = 128, and

u_defect = 9047608961789198733106474900200485 / 42535295865117307932921825928971026432.

The existing all-integer-square interpolation theorem (`two_d_theory/THEORY.md`, independently audited in `audit/BILAYER_PHYSICAL_PROOF.md`) therefore gives the displayed gap for all integer L >= 8. Its applicability is preserved here: the layer-coupling matrix has eigenvalues 2J+epsilon and epsilon, both nonnegative. The rung joint time-reversal real structure provides the required same-factor real transfer decomposition in both directions. Period-2 multiplicities are exactly those required by the transfer identity.

## 5. Short-size bridge, including the period-2 square

For J = 3/10, the unperturbed shifted H_FF has unique vacuum ground state and exact gap 2/5 for L=2, and exact gap 1 for every L>=3.

For L=2, the graph is a four-cycle with weight 2. Opposite vertices form A and B, so H_FF = Q + 2J T_A dot T_B. For q_A,q_B in {0,1,2}, the minimal scalar product is -min(q_A,q_B)[max(q_A,q_B)+1]. Enumeration gives min{1,2-4J,3-6J,4-12J}=2/5 at J=3/10, reached in the all-triplet singlet sector.

For L>=3, the four neighbours are distinct, so H_FF >= (1-5J/2)Q = Q/4. This bounds every q>=4 sector by 1. The q=1 energy is exactly 1. For q=2 at most one simple edge is active, giving energy at least 2-2J=7/5. For q=3 at most three edges are active, giving at least 3-6J=6/5. Thus the gap is exactly 1.

There are 4L^2 straight physical exchange terms counted with multiplicity. Each has minimum eigenvalue -3/4. Hence epsilon V >= -3L^2 epsilon I. Min-max gives

lambda_second(H_epsilon shifted) >= Delta_FF - 3L^2 epsilon.

The singlet product has exact expectation zero even after adding the perturbation, so lambda_ground(H_epsilon shifted) <= 0. Therefore

Delta_epsilon >= Delta_FF - 3L^2 epsilon.

This uses the zero-expectation trial upper bound, rather than paying the full perturbation spectral width. At epsilon=1/200, the L=2,...,7 lower bounds are respectively

17/50, 173/200, 19/25, 5/8, 23/50, 53/200.

Their minimum 53/200 = 0.265 exceeds the thermal bound. This closes every missing integer size and proves the all-L result stated above.

## Reproduction and status

Run, from the repository root:

python research_20261010/nonperturbative_audit/audit_ff.py --physical

The script imports no candidate-producing modules. It writes only into its own directory. BLAS/OMP/MKL are set to one thread. The recorded independent baseline run took 12.64 seconds and used 32 MiB peak RSS.

Machine-readable output: `ff_seed_J3d10_eps1d200_depth0_audit.json`.
Log: `baseline_audit.log`.

This completes the previously unaudited epsilon=1/200 candidate, including its missing finite-size bridge. It does not replace the stronger exact epsilon=0 result. Additional epsilon scans are recorded separately and do not change this fixed audited theorem.
