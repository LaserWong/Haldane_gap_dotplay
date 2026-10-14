# Audited physical proof for the weak square bilayer

## Result and exact model

On the square torus (Z/LZ)^2, put two spin-1/2 degrees of freedom at every vertex r, labeled ell=0,1. Define

H_L = sum_r S_(r,0)·S_(r,1)
    + (1/100) sum_(r,ell) [S_(r,ell)·S_(r+ex,ell) + S_(r,ell)·S_(r+ey,ell)].

The rung coupling is 1, hbar=1, and L>=2 is an integer. The sums are oriented positive-neighbor sums. When L=2, opposite starting vertices yield two equal bonds between the same pair. They are both counted. This is the size-two torus convention used throughout the physical inputs and transfer identities.

Under ordinary finite-dimensional quantum mechanics and the exact analytic inequalities detailed here and in the accompanying audit ledger, every such torus has a unique ground state and

**Delta_L >= 0.072950533962 for every integer L>=2.**

This is a genuinely two-dimensional interacting bilayer with coupling 1/100 in both unbounded directions. It is not a proof for the isotropic square-lattice Heisenberg antiferromagnet, a generic two-dimensional model, or a nontrivial two-dimensional SPT phase. No claim of a newly discovered gapped phase is made.

## An explicit time-reversal-real rung basis

In the product basis |down down>, |down up>, |up down>, |up up>, use the four orthonormal cell vectors

- (|down up>-|up down>)/sqrt(2)
- i(|down up>+|up down>)/sqrt(2)
- (|down down>+|up up>)/sqrt(2)
- i(|down down>-|up up>)/sqrt(2).

Write single-spin time reversal as J K, J=[[0,1],[-1,0]]. On the rung its linear part is J tensor J, followed by complex conjugation. Each displayed cell vector is fixed, so rung time reversal becomes ordinary conjugation. Its square is+1 even though a single spin-1/2 has time-reversal square-1.

The rung Hamiltonian is diag(-3/4,1/4,1/4,1/4) in this basis. Every individual layer spin S_ell^alpha is odd under rung time reversal and Hermitian, hence equals i A_ell^alpha with A real antisymmetric and norm 1/2. This is verified symbolically with exact rational complex entries in `independent/verify_bilayer_transfer.py`. Its output is `independent/bilayer_transfer_identity.json`.

For g>=0 each inter-rung interaction satisfies

-g sum_(ell,alpha) S_ell^alpha tensor S_ell^alpha = g sum_(ell,alpha) A_ell^alpha tensor A_ell^alpha.

All event weights are nonnegative and the two endpoint factors are identical. This is exactly the structural requirement of the self-adjoint bond-history construction, not an inference from a finite numerical spectrum.

## Transfer kernels in both directions

Fix an arbitrary integer transverse circumference W>=2 and temperature beta>0. Group W rungs in each x-column. Its on-column interaction V_W consists of W rung terms and the transverse intralayer bonds. It is real symmetric in the product of the above cell bases: each spin product uses two imaginary factors, and every interaction is Hermitian.

Across neighboring columns,

-H_cross = (g/4) sum_(y,ell,alpha) B_(y,ell,alpha) tensor B_(y,ell,alpha),

where B=2A has norm 1. There are 6W event colors. Use ordered histories with nonnegative weights g/4 per event. Their total measure is exp[(3/2)beta gW].

At a column, merge the left and right history events chronologically, place exp(-tau V_W) between events, and take the column trace. Both boundaries use the same B operators. Swapping the boundary histories leaves the merged chronological product unchanged, apart from measure-zero equal-time coincidences. The kernel is therefore real symmetric. Its absolute value is bounded by 4^W exp(beta||V_W||), so the finite-measure kernel is Hilbert–Schmidt. One simple finite bound is ||V_W||<=3W/4+3gW/2, including W=2 with its duplicated transverse terms.

The absolutely convergent Duhamel series, grouped by inter-column histories and contracted column by column, gives

Z(M,W,beta)=Tr X_(W,beta)^M for every integer M>=2.

All powers M>=2 are trace class. No positive-semidefiniteness of X is assumed. Its even powers are positive, which is what the spatial-purity argument requires. The same construction with x and y interchanged gives the corresponding exact self-adjoint transfer representation for arbitrary integer y-length. Both constructions are for the same Hamiltonian and boundary convention. Their Hilbert–Schmidt norm constants may grow with W. The ensuing purity inequalities do not require those constants to be width-independent.

These facts establish the two-direction hypotheses of the three-purity theorem, including positive odd physical traces needed to fix the sign of a unique dominant transfer eigenvalue.

## Physical heat-trace inputs with one retained vector

The finite inputs are the 2x2,4x2,4x4 rung tori, containing 8, 16, and 32 physical spins. The largest Hilbert space has dimension 2^32. For a rectangle of N rungs, let H0 be the sum of independent rung Hamiltonians. It has unique ground E00=-3N/4, gap 1, and shifted partition function

z(beta)^N=[1+3 exp(-beta)]^N.

There are 4N weak intralayer bonds, each bounded below by -3g/4. Thus V>=-3gN and ordered Weyl gives

lambda_j(H)>=lambda_j(H0)-3gN for every j.

In particular lambda1(H)>=E00+1-3gN. The product of rung singlets has weak-bond expectation zero, so lambda0(H)<=E00. For N=4,8,16 at g=.01, the second-energy lower bound lies strictly above E00. This proves the full-space unique-ground identification without assuming that a numerical symmetry block contains the ground.

The trial vectors use at most two excited rungs and total magnetization zero. Their trial dimensions are 23, 93, and 377. The basis is orthogonal but unnormalized, with exact single-rung weights 2, 1, 2, and 1. The recorded exact residual includes every state reached by H acting on the entire trial support. The corresponding union supports are 58, 1301, and 21345, not merely the trial subspaces.

The independent auditor reconstructs these maps from the explicit rung vectors and graph without importing the generating routines or diagonalizing H. It matches all exact Rayleigh quotients rho and squared residuals epsilon^2. Since rho<lambda1_lower, Temple's inequality yields

rho-epsilon^2/(lambda1_lower-rho)<=E0<=rho.

The certified lower endpoints include the nonzero residual outside the trial subspace. The small floating-point projected eigensolver proposes a vector only. All acceptance uses the saved integer vector and exact arithmetic.

Let ell<=E0<=h. The entire trace shifted by h has lower bound 1 and upper bound

Q(beta) <= exp[beta(h-ell)]
  + exp[-beta(E00-3gN-h)] ([1+3 exp(-beta)]^N-1).

The second term follows by summing the ordered Weyl inequality over all excited levels of H0, including every multiplicity. It controls the omitted 2^32-1 states without enumerating them. It is a deterministic spectral-bin bound, not a stochastic trace estimate or an assumed tail density.

## Certified seed and scalar check

At n=m=2, beta=20, independent exact replay gives

A=Z(4,2,beta)/Z(2,2,beta)^2 >=0.993912845069751,
B=Z(4,4,beta)/Z(4,2,beta)^2 >=0.987823277605056,
C=Z(4,4,2beta)/Z(4,4,beta)^2 >=0.996973815517648.

These ratios include the different finite ground-energy shifts exactly. They are not formed by treating all ground energies as E00.

One sequential three-purity cycle, with 18-digit upward rounding of defects, reaches n*=m*=4, beta*=40, and common defect

u*=844382943414457/500000000000000000 <1/500.

The checked contraction is u_(j+1)<=32u_j^2. The all-integer two-stage directional interpolation proves T(L,W,beta*)>=1-20u* for 4<=L,W<=8, and similarly at each dyadic scale. In detail, the signed y-transfer tail establishes Sx(n,W)>=1-5u. One-dimensional interpolation in y gives T(2n,W)>=1-4u. One-dimensional interpolation in x with common defect 5u gives 1-20u. Positive odd trace identities justify both dominant-eigenvalue signs. This covers every integer square L>=4, rather than only dyadic sizes.

The ratio of the first excited Gibbs weight to the largest weight is at most 32u_j. Therefore

Delta_L >= log[1/(32u*)]/40 >=0.072950533962.

The final numerical inequality was independently certified by exp[40*0.072950533962]<1/(32u*) using a positive rational Taylor enclosure, without reusing the generating logarithm implementation.

## Small-square bridge

For every square size, the same dimer-product trial and full-space Weyl bound imply

Delta_L >=1-3gL^2

whenever this right side is positive. For L=2,3 and g=1/100 it is at least 73/100. Thus the weaker 0.072950533962 lower bound applies to these remaining sizes as well. This bridge also proves their unique ground states. It is not applied at arbitrarily large area, where it would become uninformative.

## Audit artifacts and limits

- Generating certificate: `low_energy/bilayer_seed_s1d2_g1d100_relativeFalse_q2.json`.
- Independent numerical audit: `audit/independent/verify_bilayer.py` and `bilayer_g001_audit.json`.
- Exact local transfer check: `audit/independent/verify_bilayer_transfer.py` and `bilayer_transfer_identity.json`.
- The general geometric argument is separately reviewed in `audit/NEW_RESULT_REVIEWS.md`.

No large full Hamiltonian was built or diagonalized, no random confidence bound is used, and no proof-assistant formalization is claimed. The result presently concerns periodic square tori. A single square seed does not certify every arbitrary aspect ratio. The phase is a weakly coupled rung-singlet regime. Stronger coupling, topological protection, and optimality of the numerical seed are separate questions.
