# Independent counted-block theorem and physical specialization

Updated 2026-10-10 15:28 EDT (America/New_York) / 19:28 UTC.

## 1. A finite-dimensional Hermitian theorem without isolated Ritz bands

Let a self-adjoint operator H on a D-dimensional Hilbert space have the orthogonal decomposition P+Q=I, with rank(P)=r and dim(Q)>=r. In orthonormal coordinates write

H = [[A, B*], [B, C]],   C >= c I_Q.

Suppose A and B*B commute. Let a_j and v_j>0 be their simultaneous eigenvalues, with their full multiplicities, j=1,...,r. Define

ell_j = (a_j+c-sqrt((a_j-c)^2+4v_j))/2,
u_j   = (a_j+c+sqrt((a_j-c)^2+4v_j))/2.

Then every ell_j<c<u_j. If ell_(1)<=...<=ell_(r) is the sorted list, the ordered physical eigenvalues obey

lambda_j(H)>=ell_(j), j=1,...,r,
lambda_(r+1)(H)>=c.

No assumption is made about a_j<c, lambda_j(H)<c, separation of an r-level physical band, or the accuracy of P as a trial subspace.

Proof by Hermitian comparison. The exact off-diagonal block is retained:

H >= L := [[A, B*], [B, c I_Q]].

Let u_j be simultaneous orthonormal eigenvectors of A and B*B. The vectors f_j=B u_j/sqrt(v_j) are orthonormal in Q. The orthogonal two-dimensional spaces span{u_j,f_j} reduce L, with blocks [[a_j,sqrt(v_j)],[sqrt(v_j),c]]. On the remaining D-2r directions L=cI. Consequently its first r eigenvalues are exactly the lower roots, while every remaining eigenvalue is at least c. Ordered min-max comparison yields the claim.

Equivalent counted Schur proof. For any t<c, C-t>0. Congruence gives

N_H(t)=n_-[A-t-B*(C-t)^(-1)B].

Here N_H(t) counts eigenvalues strictly below t, with multiplicities. Since 0<(C-t)^(-1)<=(c-t)^(-1)I,

A-t-B*(C-t)^(-1)B >= A-t-B*B/(c-t).

Thus N_H(t) is at most the number of negative scalar terms a_j-t-v_j/(c-t), which is exactly #{j:ell_j<t}. This also gives the ordered bounds by taking t<c approaching each lower root, and N_H(t)<=r as t approaches c. This is a negative-inertia upper count, not an assertion that r physical eigenvalues occur below c.

At v_j=0 the same result follows by continuity (or by retaining the uncoupled a_j and c eigenvalues directly). All five reviewed positive couplings have v_j>0, so no singular-rank case is used.

## 2. Correct physical complement and exact matrix premises

For the periodic spin-one chain, let

H_M = sum_i S_(i,0) dot S_(i,1) + g sum_i S_(i-1,1) dot S_(i,0),
h_i = S_(i,0) dot S_(i,1)+2I.

There are M weak bonds, including both distinct links at M=2. Strong exchange is one. At M=4, D=9^4=6561, and write H'=H_4+8I. Each h_i has energies 0,1,3 with multiplicities 1,3,5. This is a weighted excitation energy, not the number of occupied dimers.

P consists of the vacuum and all twelve single-triplet basis states, hence r=13. The complement has dimension 6548 and obeys sum_i h_i>=2. In particular, it contains all twenty single-quintet states, each with weighted energy 3. An occupied-dimer count would not justify the claimed cutoff.

The independently reconstructed two-dimer physical kernel satisfies the exact positive-semidefinite inequality

V+(h_i+h_j)/2+I>=0.

The review proves this with rational LDL elimination, explicitly handling zero pivots by checking the remaining column is zero. Multiplying by g>=0, summing four edges and using degree two gives

H'>=(1-g)sum_i h_i-4g I.

For 0<=g<=1, therefore QH'Q>=(2-6g)I_Q. The producer conservatively uses b=g+10^-12 and a=g/2 in the local inequality, giving c=2-6g-4*10^-12. Its strict local positivity and all 81 LDL pivots are independently checked for every candidate.

The orthonormal P-compression and full residual Gram B*B are simultaneously diagonal in the vacuum and triplet momentum basis. They are reconstructed from all 13 exact columns, including every H-applied state outside P. The eigenchannels are:

- Vacuum: a=0, v=(16/3)g^2, multiplicity 1.
- Triplet k=0: a=1-(4/3)g, v=6g^2, multiplicity 3.
- Triplet k=+pi/2 or -pi/2: a=1, v=(32/9)g^2, total multiplicity 6.
- Triplet k=pi: a=1+(4/3)g, v=(14/3)g^2, multiplicity 3.

The review reconstructs G, K=P*VP, J=P*V^2P and R=J-KG^-1K in the rational unnormalized dimer basis. All 169 entries in each full matrix are compared, so no off-diagonal residual term is dropped. The matrix R is converted with the exact Gram weights, rather than silently treating integer Clebsch-Gordan columns as normalized. The unit strong term preserves P, so it contributes no off-diagonal residual.

At the five discrete candidate couplings, exact arithmetic verifies the ordering vacuum, k=0, k=±pi/2, k=pi of the thirteen lower roots. The triplet roots are positive and the vacuum root is negative. At g=.2, the triplet root bounds are approximately .2756360046, .5098433363 and .5423026712, respectively, whereas c is approximately .8.

## 3. Counted thermal upper bound without overlap

Let e_-<=E_0(H_4)<=rho be an independently certified full-space ground interval. The old local comparison and its full-space second-eigenvalue cutoff establish uniqueness and the validity of its Temple lower endpoint. The exact root ordering shows that the vacuum comparison root is the first ordered level. Its crude root is replaced by e_-+8; no other ordered level is removed or relabeled.

The complete weighted-reference multiplicities d_e are coefficients of

(1+3x+5x^3)^4.

They sum to 6561, with d_0=1 and d_1=12. For the producer local comparison, alpha=1-g and B=4(g+10^-12), the ordered full-space reference inequality gives lambda_j(H')>=alpha*e_j-B at every ordered index j. The first 13 indices have reference energies 0 or 1; every remaining index has e_j>=2. Therefore, for beta>0,

exp(beta*rho) Z_4(beta)
 <= exp[beta(rho-e_-)]
  + sum_(triplet channels) m_k exp[-beta(-8+ell_k-rho)]
  + sum_(e>=2) d_e exp[-beta(-8+alpha*e-B-rho)].

Exactly 1+12+6548=6561 ordered physical levels are bounded, with no gaps or double counting. The reference bins do not label the physical states or presume a conserved triplet number. They label sorted min-max bounds. The triplet contribution has precisely the multiplicities 3,6,3. Single quintets remain in the e>=2 tail through the e=3 bin.

The lower roots are enclosed downward using a rational upper bound on each square root. The review verifies the square inequalities, downward rounding, and quadratic Schur slack. It checks every exponential and thermal sum with an independent 110-term Taylor enclosure at 384-bit directed dyadic precision. Floating diagnostics are not used in any acceptance test.

## 4. Ground normalization and all-integer continuation

The normalization uses the certified small-patch rho4 without changing the physical Hamiltonian. The M8 Rayleigh quotient rho8 is rebuilt as a rational evaluation of the previously independently certified two-vector Gram/strong/weak matrix. Thus only the M8 first moment is needed; no M8 residual or omitted-band completeness is inferred.

For J=Z8(2beta)/Z4(beta)^4 and C=Z8(2beta)/Z4(2beta)^2, the numerator lower bound is exp[-2beta(rho8-2rho4)], divided by the appropriate fourth or second power of the new M4 upper trace. All shared energy shifts cancel exactly.

At the initial basepoint (4,beta), J=S(4,beta)^2 T(8,beta). Since both actual purities are at most1 at the even spatial base, this gives simultaneously S>=sqrt(J_lower), T>=J_lower, and the retained joint lower bound S^2T>=J_lower. The already reviewed signed-transfer interpolation theorem therefore covers every integer 4<=M<=8, including odd sizes.

Subsequent time-first cycles, retained joint conversion, canonical cycles, all finite windows, and the final all-integer asymptotic theorem are reused from the sealed independent joint-ratio review. The new audit replays every saved path with the new trace. Consecutive windows start at 8 and end at the exact asymptotic onset; the additional [4,8] window bridges to them. Finally the product-singlet trial and the same local form comparison give

Delta_M >= 1-(M+1)g-M*10^-12, M=2,3.

Together these cover every integer M>=2. The final accepted uniform gap is the minimum over the two short sizes, every finite window, and the asymptotic bound, rather than the asymptotic number alone.

## 5. Independent small-physical-space diagnostic

`physical_diagnostic.py` independently builds H_4+8 in the 8-spin Sz-product basis using its eight physical bonds, without using the dimer compression matrices. At g=.2, floating diagonalization in all 17 magnetization sectors gives all 6561 physical eigenvalues. Every ordered comparison bound passes, as do normalized thermal traces at beta 2,5,10,20,40,80.

The physical triplet levels of H_4+8 are approximately .6021539005 (three), .9237498779 (six), and 1.1740615947 (three). Nine of the twelve therefore exceed c≈.8. This explicitly exercises the case that invalidates a separated-low-band residual shortcut. The diagnostic is labeled floating-only and is not required for the exact theorem or gap certificate.

The exact and diagnostic checks each use at most one CPU and a 1 GiB address-space limit. Frozen predecessor artifacts remain unchanged. This is an executable exact-arithmetic mathematical certificate, not a proof-assistant formalization.
