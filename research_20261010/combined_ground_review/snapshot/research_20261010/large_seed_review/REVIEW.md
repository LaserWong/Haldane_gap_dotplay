# Independent review of larger ordinary-bilayer seeds

Updated 2026-10-10 14:07 America/New_York (EDT) / 18:07 UTC.

## Verdict

**PASS: the frozen larger-seed candidates and the separate finite-size bridges are independently verified.** For the ordinary spin-1/2 square bilayer with vertical exchange 1, equal positive straight intralayer exchange g in both directions, no crossed exchanges, and positive-direction periodic edge multiplicities (including parallel edges at length two), the resulting lower bounds are:

| g | Exact gap lower endpoint | Scope after independently checked bridges |
|---|---:|---|
| 3/100 | 0.281837226184 | Every integer square side L >= 2 |
| 1/25 | 0.179380190534 | Every integer square side L >= 2 |
| 1/20 | 0.093620600631 | Every integer square side L >= 2 |

The frozen asymptotic certificates alone start at L=8,8,16 respectively. The all-size statement additionally uses the reviewed local L=2,3 comparison and finite-window bridges described below. Each positive finite-volume gap estimate includes uniqueness of the finite-volume ground state. Neither actual-gap equality nor infinite-volume uniqueness is claimed.

The transfer, purification, and signed-transfer interpolation theorems are inherited from the existing independently reviewed two-dimensional theory. This review independently reconstructs their new physical/scalar inputs and checks the required finite-size linkage; it is not a formal proof-assistant verification.

## Frozen inputs and independence

The initial snapshot preserved 118 files. It was reconciled with the producer's 39-entry `large_seed_moments/MANIFEST_SHA256.json` and 71-entry `translation_band/FROZEN_MANIFEST_1759.json`; every hash matched. Newly supplied proof and bridge files were added without overwriting a prior snapshot. `INPUT_SHA256.json` identifies every exact byte string used. Frozen inputs are kept under `snapshot/`; no producer file was edited or regenerated.

Independent executable code here imports no producer Python module. It reuses only the frozen previous independent review's physical four-spin kernel and rational symmetric-elimination utility. The local kernel is assembled from standard physical spin exchanges in the orthonormal computational basis, rather than the production dimer implementation. The geometry C++ program was newly implemented and uses exhaustive six-site enumeration instead of the producer's generated/deduplicated reachable-mask set. Undefined-behavior/overflow sanitization was enabled.

Floating eigensolvers were not needed by the independent acceptance code. Proposed coefficient vectors and endpoints are accepted through exact integer, rational, and Q(sqrt(2)) arithmetic. Exponentials are independently enclosed using a different 384-bit, 90-term range-reduced Taylor construction, rather than the producer's 256-bit, 70-term implementation.

## 1. Exact ground moments and complete leakage

For H'=H+3N/4, write H'=Q+(g/2)A. The vacuum and spatial orbit sums of two-triplet singlet pairs form B. The additional trial vectors are L=A_42 B, with the vacuum column omitted.

Each pair is an exact total-spin-zero tensor. Consequently B and L are in the same invariant total-spin-zero, even-triplet-parity, zero-momentum sector. The (B,L) space contains q=0,2,4 states, and its complete H' image has q=0,2,4,6 support. No higher triplet-number sector can be reached in one application because each local exchange changes the number by at most two.

The matching identities were independently checked on every one of the 76 q=0,2,4,6 matching tensors on the 3x2 periodic graph, with the length-two parallel edges retained. Every symbolic image equals the image from the independently assembled physical four-spin kernel. All 225 six-triplet matching Gram entries equal 2^6 times 3 to the number of union loops. This supplements the underlying tensor identities and is not a finite-size extrapolation premise.

The newly implemented exhaustive contraction reproduces F=L*L, S=L*A_44L, V=(A_44L)*(A_44L), and W=(A_64L)*(A_64L) exactly on 2x2,4x2,4x4,8x4,8x8. In particular, it visits all C(64,6)=74,974,368 six-site subsets on 8x8 and finds exactly 10,585,856 active ones, matching the producer without using its reachability construction. Every F/S/V/W integer agrees.

The complete G,K,J matrices were independently assembled by separating the q<=2, q=4, and q=6 components of the H' images. The q6 Gram W is included in J; J is not the square of the compressed Hamiltonian. The original B-space M0 through M4 were then reconstructed and compared entry-for-entry.

All 15 files at g=.01,.02,.03,.04,.05 on 4x4,8x4,8x8 passed. Exact Gram elimination independently reproduces every selected basis index. Their linear trial dimensions are 11,29,29. Full Hilbert dimensions are 4^16,4^32,4^64; physical spin counts are 32,64,128. Each ground file retains one proposed ground state, with no MPS representation or MPS bond dimension.

The coefficient-vector norms, Rayleigh quotients, full residual squares, local relative-form positivity, all-sector affine thresholds, and every applicable Temple interval were independently replayed. Files whose old affine threshold is insufficient correctly contain no Temple lower endpoint. Their exact moments remain valid, and the full-band calculation instead uses the stronger reviewed number-sector cutoff.

## 2. Translated complete spin-1 band

For a localized bare triplet v_r with magnetization +1, let C_+=sum_q P_(q+2) H' P_q and w_r=(I-C_+/2)v_r. H' and each P_q commute with total spin, so w_r has spin 1. The independent audit additionally verifies total S+ w_r=0 exactly and magnetization +1 on every support state. The rational raising coefficients are 1 for triplet- to triplet0 and 2 for triplet0 to triplet+.

The q=1 part of w_r is exactly v_r. Hence all N translations are linearly independent for every coupling in scope. The lowering maps are spin-1 isometries after normalization and commute with H' and translation; this gives exactly three orthogonal copies with identical moments. This is an exact symmetry multiplicity, not numerical degeneracy. Ground and triplet trial blocks are orthogonal by parity and total spin.

All nine sparse W=2d w and dH'W columns at three geometries and three couplings were independently rebuilt using the physical local kernel. They agree entry-for-entry with the stored columns, including all q=5 leakage. On N=16,32,64 their trial supports are 85,181,373 and their full reached supports are 3,185,15,466,67,755.

Every displacement correlation G,A,B was then recomputed, including all displacements rather than only reflection representatives. Translation bit permutations were independently verified on every single-site local basis digit, which proves the permutation on all product states. Exact Fourier evaluation independently reproduces all G(k),A(k),B(k), theta(k), residual squares, and rational outward endpoints in Q(sqrt(2)). Every G(k)>0 and residual square >=0. The N complex Fourier sectors count N independent directions; there is no additional factor for a conjugate momentum pair.

## 3. All-Hilbert-space spectral count

The local number-preserving inequality V_pres >= -(Q_i+Q_j)/2 was independently checked by rational inertia. There are exactly three normalized pair-creation coefficients, each with squared magnitude 1/4 at unit g. These yield H'_(q,q)>=(1-2g)q and

||P_(q+2)H'P_q||^2 <= (3g^2/4) E_empty,upper(q) E_occ,upper(q+2).

The geometry bounds used here are true upper bounds, not purported exact occupancy maxima. For a q-vertex subset of the degree-four torus, 4q=2e(q)+boundary. With h=min(q,N-q), the row/column argument proves boundary/2 >= min(ceil(2 sqrt(h)),nx,ny):

* With no full row or full column, all occupied rows/columns are partial, so boundary/2 >= r+c >= ceil(2 sqrt(q)).
* With a full row but no full column, every column is partial; transpose for the other case.
* With both a full row and a full column, no row or column is empty. The complement lies in the intersections of partial rows and columns, so r c >= N-q >= N/2 and r+c >= sqrt(2N) >= min(nx,ny).

Complementation covers q>N/2. Length-two cycles retain two boundary edges, so their multiplicity convention is consistent. For the simple even-sided larger graphs, bipartiteness also gives e(q)<=floor(q^2/4), and degree gives e(q)<=2q. The complementary identity e(q)=4q-2N+e(N-q) is applied safely. Taking the minimum preserves an upper bound.

Every saved diagonal, off-diagonal square, parity-chain lower endpoint, positive rational LDL pivot, monotonicized spectral bin, combinatorial multiplicity, and first ordered index was recomputed. The multiplicities sum to the full 4^N, including all spin and magnetization sectors. Min-max on the codimension sum_(j<q) C(N,j)3^j compression has the correct direction: its lower bound implies lambda_(codimension+1)>=a_q.

Let a0,a1,a2 be the first three global bins. The singlet trial has rho<a1, while lambda2>=a1, so the unique ground is in its invariant sector. All 3N triplet trial Ritz values lie below a2. Together with the ground trial they give exactly k=1+3N eigenvalues below a2 because the full-space bound is lambda_(k+1)>=a2. Each represented momentum/spin sector has exactly one such eigenvalue, and every unrepresented sector has spectrum >=a2. This closes the missing-state loophole before any residual estimate or tail truncation is used.

## 4. Sector complements and endpoint direction

In the unique ground sector the lower spectral floor is a0; in each triplet sector it is a1. Their rank-one residual-angle bounds therefore give

b0=a2-(a2-a0) r0^2/(a2-rho)^2,

bk=a2-(a2-a1) rk^2/(a2-theta_k)^2.

The saved rational upper residual/energy endpoints safely enlarge the ratios, whose denominators are verified positive. Every angle bound is below one. Taking the minimum of these b values also covers all unrepresented sectors because they already have spectrum >=a2. All these inequalities and fractions reproduce exactly.

For every ground or triplet lower endpoint l, the audit explicitly checks l<b, l<=theta, and (b-l)(theta-l)-r^2>=0 in exact arithmetic. Thus the accepted endpoint is on the correct lower quadratic branch. All frozen endpoints pass. As code hardening, future producer acceptance should explicitly retain these branch checks rather than relying on the floating proposal to select the intended branch; this is not a defect in any frozen endpoint.

## 5. Heat trace, purification, and integer-size bridge

Only after the preceding global count is established may the tail start at q=2. The complete ground-plus-triplet band supplies both lower and upper heat-trace contributions with multiplicities 1 and 3. The positive tail sum uses C(N,q)3^q exp[-beta(a_q-u0)], q>=2. No subtraction of outward interval estimates is used.

The independent exponential implementation reproduces all stored 16-decimal downward J1,J2,C ratios, all first-cycle purities, every rounded scalar recurrence step, and every final gap endpoint. The canonical cancellation identities are unchanged for the larger 4x4,8x4,8x8 family, but the first updated side is 8 and temperature is 2 beta0. The final onsets are 8,8,16, as stored. A separate exponential test verifies exp(beta_final gap)32u<1 without trusting the stored logarithm.

The independent bridge review then checks:

1. The exact full four-spin matrix M=V+(3/2)(Q_i+Q_j)+I/3 is positive definite. Summing gives H'>=(1-6g)Q_total-2Ng/3. Full-space min-max and the product-singlet upper energy 0 imply gap>=1-(6+2L^2/3)g. The L=3 values .64,.52,.40 safely cover both L=2,3, even though L=3 is not bipartite.
2. At base side 4, J1_true=A^4 B^2 C with 0<A,B,C<=1 implies every true A,B,C is at least the certified J1 lower bound. Therefore the conservative (J1,J1,J1) base triple is valid; it must not be confused with the first updated side-8 triple.
3. Every saved signed-transfer finite-window square-root witness and every proposed gap is independently accepted by rational inequalities and the independent exponential enclosure. The base windows give .337867884900,.264039251376,.188350474715; the needed g=.05 side-8 window gives .169897925769. Each exceeds its final asymptotic bound.

These intervals cover L=2,3, then L=4..7, then L=8..15 when needed, followed by every larger integer. `results/all_size_bridge_review.json` records the resulting all-L>=2 endpoints.

## 6. Independent review of the new moment lemmas

The producer's stronger lemmas are **analytically valid**, but were not used in the frozen angle-based numerical certificates above.

For H=[[T,R*],[R,C]], suppose lambda_(k+1)(H)>=a and T<aI. Min-max gives lambda_k<a, hence H-a has exactly k strictly negative eigenvalues. Elimination of the invertible negative block T-a yields

neg(H-a)=k+neg(C-a+R(a-T)^(-1)R*).

The latter Schur complement must be positive semidefinite, even if H has eigenvalues exactly at a. Thus C>=aI-R(a-T)^(-1)R*, and in particular C>=[a-epsilon/(a-r)]I if R*R<=epsilon I and T<=r<a. This needs no global lower spectral floor. In invariant rank-one sectors the correction is r_j^2/(a-theta_j).

For the inverse-moment statement, K=A-aG<0, X=(H-a)W, and S=X*X=B-2aA+a^2G>0. Full rank of X follows because Xc=0 would force c*Kc=0. The Moore-Penrose inverse M=(H-a)^dagger has exactly k negative eigenvalues, ordered nu_j=1/(lambda_(k+1-j)-a). Its compression to ran(X) has generalized Ritz pencil (K,S), with nu_j<=mu_j<0. The decreasing reciprocal on the negative half-line then gives lambda_i>=a+1/mu_(k+1-i). For l<a, a strict sufficient condition is

neg[B-(a+l)A+alG] >= k+1-i.

Multiplication from K-S/(l-a) uses the positive factor a-l, so the sign is correct. Eigenvalues of H exactly equal to a map to zero and do not alter the negative count. At k=1 the formula is exactly Temple, rho-r^2/(a-rho). Any numerical variant using this improvement requires its own new endpoint/trace replay; analytic acceptance alone does not promote its numbers.

## Reproduction and resources

Run `REPRODUCE.sh` from any directory. It compiles the independent C++ checker locally, verifies frozen input hashes, rebuilds the exhaustive geometry, and replays local/ground/translation/tail/trace/bridge checks. Outputs go only to this review directory. No remote state changes occur.

All compute is pinned to one CPU, all BLAS/OpenMP thread counts are one, and address-space limits are at most 1.5 GiB (the reused independent kernel further restricts Python audits to 1 GiB). The 8x8 exhaustive sanitized geometry run took about 90 seconds and 11 MiB peak child RSS under shared load. Sparse translation replay took roughly 18-31 seconds per 8x8 coupling. These are observed run costs, not machine-independent benchmarks.
