# Independent stronger-coupling chain review

Date: 10 October 2026. This is an extension of the independent chain audit. All three positive candidates and all three recipe obstructions below have passed independent exact-arithmetic review. Exact inputs, final replay status, and resource measurements are in `summary.json`, `INPUT_SHA256SUMS.json`, and the individual review JSON files.

## Model and normalization

The model is the periodic spin-one alternating Heisenberg chain with M two-spin cells, strong coupling 1 and weak antiferromagnetic coupling g. In a dimer relabeling,

H_M = sum_i (S_{i,0} . S_{i,1}) + g sum_i (S_{i-1,1} . S_{i,0}).

There are 2M physical spins and full dimension 9^M. Both distinct inter-dimer edges are retained at M=2. This is the same model and boundary convention as `../chain_audit/CHAIN_CERTIFICATE_PROOF.md`. All results concern every integer M>=2, including odd M, after their finite windows and short bridges pass. They are sufficient certificates, not physical phase boundaries or optimal-coupling claims.

## Independent implementation and exact finite inputs

`independent_core.py` is copied from the previous independent auditor `../chain_audit/verify_chain.py`, with only the input directory and 1 GiB address-space limit changed. `independent_core_changes.patch` makes every change explicit. `verify_frontier.py` imports this independent core and no producer mathematical module.

The core rebuilds the nine unnormalized dimer columns directly in the physical spin basis. It verifies their norms, orthogonality, and strong-dimer eigenvalue equations. Excitation energies are 0,1,3 with multiplicities 1,3,5. It independently reconstructs spin operators and the weak Heisenberg matrix, retaining the positive diagonal Gram metric.

For each supplied integer trial vector v it reconstructs Hv on the entire reached support, including configurations outside the trial space. Its exact rational Rayleigh quotient and full residual square are compared with the supplied records. The periodic edge multiset is checked directly. It tests the local comparison

g V + a(h_i+h_j) + b I > 0

by exact rational LDL elimination of independently reconstructed physical-magnetization blocks. All 81 pivots must be positive. Summation yields

H_M >= -2M + alpha sum_i h_i - M b,  alpha=1-2a>0.

The full reference bins are coefficients of (1+3x+5x^3)^M, whose total is independently checked as 9^M. Therefore the second physical eigenvalue is at least c_M=-2M+alpha-Mb. A trial quotient rho<c_M proves a unique ground state, with exact Temple enclosure

e_- = rho-R^2/(c_M-rho) <= E0 <= rho=e_+.

No spectral-completeness inference is drawn merely from a small residual or the magnetization-zero trial space.

## Full thermal tails and cancelled first step

Write Q_M=exp(beta e_+) Z_M(beta). The audited ground enclosure and complete ordered reference bins imply

Q_M <= exp[beta(e_+-e_-)] + exp[-beta(-2M-Mb-e_+)] [(1+3 exp(-alpha beta)+5 exp(-3alpha beta))^M-1] = Q_M^+.

The subtraction removes exactly the unique lowest reference level. Every omitted physical level is included in the remaining ordered bound.

For seed sizes n=4 and 2n=8, the conventional ground-only lower inputs are

S = exp[-beta(e_+(2n)-2e_+(n))]/(Q_n^+)^2,
T = 1/(Q_2n^+)^2.

There is a stronger directly cancelled first spatial argument:

J = exp[-2beta(e_+(2n)-2e_+(n))]/(Q_n^+)^4.

This is a rigorous lower bound for S(n,2beta). Indeed Z_n(2beta)<=Z_n(beta)^2, so

S(n,2beta)=Z_2n(2beta)/Z_n(2beta)^2
          >= Z_2n(2beta)/Z_n(beta)^4
          >= exp[-2beta e_+(2n)]/[exp(-beta e_+(n)) Q_n^+]^4.

It avoids introducing and then separately bounding the cancelling Z_2n(beta) factor. It does not assume that an unknown thermal purity equals one.

For G(x)=1-(1-x)^2/(2x^2), the first canonical state at (2n,2beta) is

A=G(J),  B=G(T^2 A).

The squaring inequality itself follows for any probability weights x_i: writing P=sum_i x_i^2, one has

1-sum_i x_i^4/P^2 = 2 sum_(i<j) x_i^2 x_j^2/P^2
                  <= 2(sum_(i<j) x_i x_j)^2/P^2 = (1-P)^2/(2P^2).

Thus squaring and renormalizing raises purity to at least G(P), and G is increasing on (0,1]. The even spatial powers are probability spectra even when the underlying transfer has negative eigenvalues. The exact exchange identity is

T(4n,beta)=S(2n,2beta) T(2n,beta)^2 / S(2n,beta)^2 >= A T^2,

because S(2n,beta)<=1. Thermal squaring then supplies B. These spatial- and thermal-squaring inequalities use the newly computed spatial input in the thermal update. Subsequent sequential updates are independently reconstructed with 12-decimal outward rounding. Every producer lower endpoint is independently validated, every nonlinear update is reproduced exactly, and each accepted final gap d is checked by an independent rational exponential enclosure:

exp(beta_final d) < 1/(5u),  u=max(1-S_final,1-T_final)<=1/100.

The known all-integer signed-transfer interpolation then covers every M>=n_final. The self-adjoint transfer representation is inherited from the already reviewed homogeneous exchange- and cell-time-reversal-invariant Heisenberg model; the old analytic seed's width restriction is not a transfer restriction.

The producer uses 128-bit exponential enclosures. At some large, rejected temperatures they are looser than the independent 80-decimal enclosure, so the three pre-update rounded endpoints need not coincide. The audit checks the required lower-bound direction explicitly, then reproduces the producer's nonlinear updates from those verified endpoints. No producer arithmetic is imported or trusted for acceptance.

## Finite windows and M=7

For any canonical state (S,T) at even n with P=S^2 T>1/2, define

w=(1+sqrt(2P-1))/2, r=(1-w)/w, D=T/(1+r^2),
C=(1-r) min(S sqrt(D),D).

The independently reviewed finite-window lemma in `../root_review/FINITE_WINDOW_INTERPOLATION.md` gives T(M,beta)>=C for every integer n<=M<=2n. Its proof allows signed transfer spectra: the unique largest-modulus eigenvalue is positive because all sufficiently large odd physical traces are positive; the other absolute eigenvalue powers are bounded by r. Absolute-spectrum Holder interpolation is used only between even endpoint powers. There is no positivity assumption on the full transfer spectrum.

This review computes both square-root lower endpoints by exact integer square roots at 60 decimal places and checks both neighboring-square inequalities. It proves every producer window purity lower endpoint is below this independent enclosure. Each advertised window gap is then verified by

exp(beta d)(1-C_saved)<C_saved.

The windows are explicitly checked to be contiguous from M=8 to the first all-large-size accepted M. Their temperature and canonical inputs are compared with the separately audited scalar replay.

For g=.16, an independently positive local comparison and singlet-product trial prove Delta_M>=1-2a-Mb through M=7. For the stronger .161 and .16125 candidates, that local bridge is used for 2<=M<=6. A separate M=7 integer trial with full residual support is audited; its gap is directly c_7-rho. This closes the potentially missed odd-size endpoint. The minimum of every short, window, and asymptotic lower bound is checked against the claimed all-size number.

## All-beta, all-local-parameter obstruction

The obstruction concerns only the specified ground-only numerator, independent-dimer-bin tail, and standard or cancelled-first-step G-recursion. It does not establish gaplessness, exclude other trace estimates, larger seeds, low excited-state numerators, altered recursion, or all couplings above a threshold.

For an arbitrary valid local comparison, let lambda_min(a) be the lowest eigenvalue of gV+a(h_i+h_j). Necessarily b>=-lambda_min(a), so

c_M+2M = 1-2a-Mb <= 1-2a+M lambda_min(a).

For any nonzero rational vector u in the local weighted dimer basis, the variational inequality yields the all-real-a affine upper bound

1-2a+M lambda_min(a) <= 1+M <gV>_u + a(M<h_i+h_j>_u-2).

The producer supplies two integer vectors whose affine slopes have opposite signs. This review reconstructs each norm and both expectations using its own physical kernel. The minimum of the two lines has a global maximum at their intersection, giving a rigorous constant C_M with c_M<=-2M+C_M for every real a. In particular it covers every allowed positive-alpha comparison and permits different local parameters at different sizes and temperatures. No floating optimizer is part of the proof.

Let baseline ground intervals be [l_M,u_M]. Even allowing arbitrarily sharp refinements of both ground bounds anywhere within those intervals, and optimistically discarding all ground-width penalties, define

delta_M=-2M+C_M-l_M, kappa=l_2n-2u_n>0.

The first triplet reference bin alone forces the recipe denominator to satisfy

Q_M^+ >= q_M(beta):=1+3M exp(-beta delta_M).

Thus its best possible cancelled argument and thermal input obey

J_recipe <= exp(-2beta kappa)/q_n(beta)^4,
T_recipe <= 1/q_2n(beta)^2.

The same upper envelope covers the standard first-step recipe, since its extra denominator is >=1 and G is increasing on (0,1]. These are bounds on what the certificate recipe can produce, not upper bounds on the physical purities.

For a rational interval [l,h], the audit uses the endpoint giving the smallest q_M (h if delta_M>=0, l otherwise) and exp(-2l kappa) for the numerator. Its independently enclosed J,T upper bounds must lie below the saved rational upper endpoints. It propagates the latter with independently implemented upward 12-decimal rounding, rather than the producer's 128-bit rounding. Rejection requires a mathematically terminal event:

- a nonpositive upper bound for the proposed first or subsequent G-step; or
- S^2 T<=1/2, an absorbing failure region disjoint from acceptance.

For the latter, the next spatial upper bound is <=G(1/2)=1/2, and the thermal upper bound is also <=1/2. The next product is then <=1/8, so this region cannot approach the acceptance requirement S,T>=.99. Likewise J<=1/2 immediately leads to failure after the cancelled first step. An iteration-budget exhaustion is never accepted as an exclusion.

The .1625 certificate is checked on the exact contiguous interval union [0,64], [64,80], [80,88], [88,96], [96,112], [112,128], [128,256]. Beyond beta=256, exp(-2beta kappa)<=exp(-512kappa)<=1/2 supplies the analytic tail. The checker independently requires no unresolved or unvisited intervals.

At g=.175, the independently reconstructed eight-dimer ceiling gives a direct split at beta=128: below the split the recipe's T upper bound is <=1/2, making its first thermal step nonpositive even with J=1; above the split the J upper bound is <=1/2. This covers every beta>0. The beta=0 endpoint is included only for interval enclosure, not as an admissible positive-temperature seed.

At g=.1615, the depth-four ground intervals were inconclusive. A subsequently finalized depth-five input has now passed this independent audit: 33 contiguous rational intervals cover [0,256], and the same analytic high-beta argument covers [256,infinity). Its M=8 full residual is independently reconstructed from a 245,870-dimensional trial and reaches 939,326 configurations. Sharpening those depth-five ground intervals arbitrarily cannot overcome this recipe obstruction. The earlier depth-four inconclusiveness was never treated as an exclusion. These isolated-coupling results do not prove monotonicity in g or identify an exact maximal coupling.

## Reproduction

From the repository root:

    PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
    taskset -c <one permitted CPU> python research_20261010/chain_frontier_review/verify_frontier.py --include-new --include-deeper

The process caps its address space at 1 GiB. NumPy is used only to read saved integer npz vectors; no eigensolver is called. The output contains exact fractions, all LDL pivots, all finite-window square-root enclosures, every interval rejection trajectory, input hashes, and measured peak RSS. No archived input file or producer file is changed. This is an executable exact-arithmetic certificate, not a proof-assistant formalization.

## Verified three-candidate finite-window values

The completed initial replay audited 195 inverse-temperature entries (65 per coupling), including 25 accepted entries. All selected below pass.

| g | Initial beta | Asymptotic starting M | All-M>=2 gap | Combined short bridge gap |
|---|---:|---:|---:|---:|
| 4/25 = .16 | 80 | 64 | .004358246531 | .006304485945 |
| 161/1000 = .161 | 86 | 128 | .001952374069 | .078455042436 |
| 129/800 = .16125 | 88 | 256 | .001075806295 | .077023921872 |

The successive windows begin at M=8 and double:

- g=.16: [8,16] .004786281211; [16,32] .004941728136; [32,64] .005042826756.
- g=.161: [8,16] .002091566879; [16,32] .002071786100; [32,64] .002203063550; [64,128] .002269157163.
- g=.16125: [8,16] .001283948378; [16,32] .001095353433; [32,64] .001126137799; [64,128] .001202344641; [128,256] .001232945173.

Every window gap exceeds its row's asymptotic gap. For each coupling the largest accepted trial has dimension 43,294 and full residual support 245,870 within full Hilbert dimension 43,046,721. The separate M=7 trials used in the last two rows have dimension 365, full reached support 3,683, and full Hilbert dimension 4,782,969. These are linear support sizes; no MPS bond dimension is being reported.

The final clean combined replay completed in 187.25 seconds with peak RSS 303.3 MiB, one-CPU affinity, BLAS threads one, and a 1 GiB address-space cap. All nine record hashes explicitly supplied as finalized by the producer matched; remaining trial and parent-record hashes are also saved.
