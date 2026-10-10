# Counted small-patch triplet comparison for the spin-one chain

Updated 2026-10-10 15:30 America/New_York (EDT) / 19:30 UTC.

Status: exact producer candidates; independent external review pending. All frozen inputs of `chain_filter_extension` remain unchanged.

## Results and scope

| g | All-integer M>=2 gap candidate | Initial beta | Extra time-first / canonical cycles | Asymptotic onset |
|---|---:|---:|---:|---:|
| .18 | .112949677804 | 11.2 | 3 / 0 | M>=64 |
| .185 | .096048414952 | 11.45 | 3 / 0 | M>=64 |
| .19 | .078956697835 | 11.75 | 3 / 0 | M>=64 |
| .195 | .061526095375 | 12.2 | 3 / 1 | M>=128 |
| .2 | .043446395688 | 12.75 | 3 / 1 | M>=128 |

These are five discrete sufficient certificates, not a continuous-coupling interval or an estimate of the actual physical gap. Every claimed finite volume has a unique ground state. No infinite-volume uniqueness or phase boundary is claimed.

The physical model is the periodic alternating spin-one chain

H_M(g) = sum_i S_(i,0) dot S_(i,1) + g sum_i S_(i-1,1) dot S_(i,0).

Strong exchange is exactly 1. There are 2M physical spins and full dimension 9^M. Every one of the M oriented periodic weak links is retained, including both distinct physical links at M=2. The weak operator is one physical spin-one Heisenberg bond, not the sum of two bilayer bonds.

## 1. Only thirteen new reference trial vectors

For the denominator patch M=4, shift H'=H_4+8 and write H'=E+gV. The strong excitation E is the sum of four dimer energies 0,1,3, with multiplicities 1,3,5.

Let P project onto E<2: the vacuum plus four positions times three magnetic components of a single triplet. Thus rank(P)=13 and rank(Q)=6,548 for Q=I-P. The twenty one-quintet states have E=3 and belong to Q. The complement is determined by excitation energy, not by the number of occupied dimers, and no number-parity conservation is assumed.

The thirteen rational bare vectors have total configuration support 13. Exact full H' action has union support 172, or 173 for the unshifted H because the vacuum diagonal is then nonzero. The full residual union has support 160. No full-space diagonalization supplies a certificate. A supplemental sparse benchmark uses the 1,016-dimensional Sz=1 block and its 254-dimensional momentum blocks; its eigenvalues are labeled floating diagnostics only.

The dimer basis uses the physical integer Clebsch-Gordan columns and Gram weights (3,2,2,2,1,2,6,2,1) from the independently reconstructed chain kernel. Vacuum metric norm is 81 and every bare single-triplet norm is 54. All scalar products below use this metric.

The producer reconstructs the exact Gram diagonal G, first weak moment K=<V>, and full second weak moment J=<V*V>. The full residual Gram is

E_R = J - K G^-1 K.

All leaked configurations enter J; replacing J by a square of the compressed first moment would invalidate the result. Strong excitation maps P into itself, so the full H' residual Gram is exactly g^2 E_R.

## 2. Exact normalized channel data

The vacuum and the three Sz triplet blocks are orthogonal. Their first-moment and residual-Gram cross blocks vanish exactly. The three triplet blocks are identical real symmetric circulant four-by-four matrices. The Fourier eigenvalues therefore diagonalize both first moment and residual Gram simultaneously. No numerical eigenvectors or inferred spin assignments are used.

| Channel | Multiplicity | theta=<H'> | Full residual variance |
|---|---:|---:|---:|
| Vacuum | 1 | 0 | (16/3)g^2 |
| Momentum 0 triplet | 3 | 1-4g/3 | 6g^2 |
| Momenta ±pi/2 triplet | 6 | 1 | (32/9)g^2 |
| Momentum pi triplet | 3 | 1+4g/3 | (14/3)g^2 |

The multiplicity six is two conjugate momentum channels times three magnetic components. These thirteen comparison channels need not coincide with thirteen isolated physical eigenvalues below the next comparison cutoff.

## 3. A rigorously counted omitted-state cutoff

For one oriented weak bond the normalized local spin-one operator obeys

V_local + (h_i+h_j)/2 + I >= 0,

where h_i is the strong-dimer excitation. The independent reviewer also checks this exact semidefinite statement. For simple strict-LDL acceptance the producer uses the slightly weaker rational inequality

g V_local + (g/2)(h_i+h_j) + (g+10^-12) I > 0.

All 81 exact weighted local pivots are positive. Summing the four periodic edges yields

H' >= alpha E - B I,
alpha=1-g, B=4g+4*10^-12.

On ran(Q), E>=2, hence

QH'Q >= A Q, A=2-6g-4*10^-12.

This is a compression bound. E need not commute with H'. Globally, Courant-Fischer supplies lambda_14(H')>=A because P has dimension thirteen.

The same local comparison supplies every higher ordered reference bin. The complete multiplicities are the coefficients of

(1+3x+5x^3)^4.

Their sum is 6,561; bins E=0 and E=1 contain respectively one and twelve states. The E>=2 bins contain exactly 6,548 states, including all quintets.

## 4. Counted Schur lower roots without band isolation

Use normalized P coordinates and write the full physical block matrix as

H' = [[D,R*],[R,C]], with C>=A I_Q.

D is the normalized first moment and R is the full residual map. The direct block Loewner inequality

H' >= [[D,R*],[R,A I_Q]]

is valid because their difference is diag(0,C-A I_Q)>=0. Since D and R*R commute in the exact channels above, each channel with mean theta and variance v contributes a two-by-two comparison block with diagonal entries theta,A and off-diagonal magnitude sqrt(v). Its smaller eigenvalue is

ell = (theta+A-sqrt((theta-A)^2+4v))/2 < A.

The larger root is above A; the rest of the complement comparison spectrum is A. Consequently the first thirteen physical ordered eigenvalues are bounded below by the sorted thirteen lower roots, and all remaining physical eigenvalues are at least A.

Equivalently, for every t<A, C-t>0 and

D-t - R*(C-t)^-1 R >= D-t - R*R/(A-t).

The negative inertia of the right side bounds the number of full H' eigenvalues below t from above. Each scalar channel becomes negative only after t exceeds its lower root. This proves the ordered count independently of where the actual upper triplet eigenvalues lie relative to A.

In particular, the argument does not require the maximum retained Rayleigh quotient to be below A, an assumption that fails here for a direct Temple-style isolation of the full thirteen-state band. At g=.2, A is just below .8, while the floating higher triplet energies are about .924 and 1.174. Those diagnostics illustrate the distinction; they do not enter acceptance.

For exact arithmetic, the discriminant square root is rounded upward on a 10^-30 rational grid, then ell is rounded downward to 24 decimal places. Every saved endpoint satisfies ell<A and

(theta-ell)(A-ell) >= v.

The lower branch and root witnesses are checked exactly. All five parameter points have the channel ordering vacuum, momentum 0, momenta ±pi/2, momentum pi. The accurate independently certified M=4 ground lower bound from the existing small trial is above the vacuum comparison root and below the first triplet root. It can replace only the first ordered lower endpoint. No extra state is subtracted and no ground or triplet contribution is double counted.

## 5. Complete trace bound and unchanged large numerator

Let rho4 be the old exact small-patch Rayleigh upper endpoint and e_- its full-space Temple lower endpoint. Let ell_0, ell_1, ell_2 denote the three triplet comparison roots, with multiplicities 3,6,3. Then for beta>0,

exp(beta rho4) Z4(beta)
<= exp[beta(rho4-e_-)]
 + 3 exp[-beta(-8+ell_0-rho4)]
 + 6 exp[-beta(-8+ell_1-rho4)]
 + 3 exp[-beta(-8+ell_2-rho4)]
 + sum_(e>=2) m_e exp[-beta(-8+alpha e-B-rho4)].

Every term is positive and outward rounded separately. At beta=0 the count is exactly 1+3+6+3+6,548=6,561. The complete reference bins account for every omitted physical state; no sampled Ritz list replaces this count.

At g=.2 the three rigorous shifted triplet lower endpoints are approximately .2756360046, .5098433363, .5423026712. The old first-bin bound was only about .0834. The substantial denominator improvement comes from the full residual comparison and complete count, not from changing the almost-exact M=4 ground endpoint.

The M=8 numerator is exactly the saved Rayleigh trial from the frozen two-vector moment package. Its full support remains 43,294 in the 43,046,721-dimensional physical space. New candidates recompute only its two-dimensional rational energy formula at the chosen g. They do not reconstruct its support, apply H to it, claim a new residual, or use a large energy lower endpoint.

## 6. Scalar cycles and all integer bridges

The sealed `chain_filter_extension` joint-purity identities and exact recurrence are reused unchanged. The only changed physical input is the complete M=4 trace upper bound above. Initial J and C, all repeated temperature-first cycles, conversion with retained joint endpoint, and all later canonical cycles retain their original space/temperature basepoints.

A further simple initial bridge closes the smaller cell counts without new M=5,6,7 trial states. At v=(M=4,beta), define

J_actual = Z8(2 beta)/Z4(beta)^4 = P_x(v)^2 P_t(D_x v).

If J is its certified lower endpoint, both individual purities are <=1, so at that same base

S>=sqrt(J), T>=J, and S_actual^2 T_actual>=J.

The independently reviewed joint-aware signed-transfer finite-window lemma then covers every integer 4<=M<=8 at inverse temperature beta. This includes M=5,6,7, with no parity assumption. At g=.2 its gap lower endpoint is .049623310790, larger than the final uniform candidate.

For M=2 and M=3, use the same local comparison and the singlet-product quotient -2M. The second eigenvalue cutoff gives

gap_M >= 1-(M+1)g-M*10^-12.

These bounds are positive and exceed the reported uniform gap at all five points. The original [4,8] window, every subsequent [8,16],[16,32],... window, and the terminal all-integer asymptotic theorem are contiguous. Every reported gap is certified by an exact rational exponential inequality. The producer compares several earlier and later valid terminal rounds to avoid a threshold stopping artifact.

## 7. Verification, resources, and freeze

`unit_moments.json` stores the complete exact thirteen-state physical input. `patch_g*.json` stores the cutoff, roots, multiplicities, full reference bins and unchanged ground/numerator inputs. `candidate_g*.json` records every accepted exact path and all bridges. `verify_composition.py` separately checks the channel/root arithmetic, every M=4 full residual and local LDL, the unchanged two-dimensional largest energy, complete trace, every scalar path and all short/window bridges. An external reviewer independently reconstructs all thirteen-state physical moments and reviews the comparison theorem.

All executables use one permitted CPU, one BLAS/OpenMP thread, and a one-GiB address-space ceiling. `summary.json`, `resources.json` and `verification.json` record observed costs. The sparse benchmark is separate and does not supply a rigorous acceptance condition. No full M=4 spectrum or new M=8 support is computed. This is a scalable finite-reference-subspace and omitted-compression method, specialized here to a particularly small denominator patch.

The prior producer manifest SHA-256 is bc1b7bcc23f7f217c558a77790c0c45a8763ae40c1d8b20b5ca3b50d18d16370. Every old frozen byte is checked before scalar reuse. The new package has its own external-input and frozen-file manifests. The working tree has no Git metadata, and no remote publication is implied.
