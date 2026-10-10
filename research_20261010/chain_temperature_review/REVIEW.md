# Independent review: temperature-first spin-one chain certificates

Updated 10 October 2026, 14:46 America/New_York (EDT) / 18:46 UTC.

## Verdict

The periodic spin-one alternating Heisenberg chain with strong exchange 1 has a unique finite-volume ground state and the following rigorously certified gap for **every integer two-spin cell count M >= 2**:

| Weak exchange g | Gap lower bound | Initial beta | Canonical asymptotic onset |
|---|---:|---:|---:|
| 323/2000 = .1615 | .039815121561 | 39/2 | M >= 32 |
| 13/80 = .1625 | .037716426713 | 81/4 | M >= 32 |
| 7/40 = .175 | .006791087005 | 23 | M >= 128 |

All intervening sizes, including odd M, pass the finite-window and short-size bridges below. These are sufficient certificates at three discrete couplings, not a continuous-coupling statement, estimate of the physical gap, or optimal-coupling claim. The bounded g=.2 scan has no accepted point; it is **not an all-beta obstruction**.

The earlier space-first obstructions at these couplings remain correct for their specified ground-only numerator, independent-dimer-tail, canonical-order recipe. They do not exclude the present temperature-first construction. No old obstruction or frozen input was changed.

This is an exact-arithmetic certificate and analytic independent review, not a proof-assistant formalization.

## 1. Model, physical normalization, and source integrity

The exact Hamiltonian is

H_M(g) = sum_i S_(i,0) dot S_(i,1) + g sum_i S_(i-1,1) dot S_(i,0),

on periodic cells i modulo M, with physical spin one at each site. Strong coupling 1 fixes the energy unit. There are 2M spins and full Hilbert dimension 9^M. At M=2 the two distinct oriented weak links are both retained; the periodic edge multiset is not deduplicated. Interpolation concerns cell counts, not arbitrary microscopic lengths.

The producer explicitly froze 14 files, with manifest SHA-256

2aed748169de52b5a2acce733abecbeb491f309229545404295b38262f0cc915.

All 14 frozen files were copied into `snapshot/` and checked against that manifest. All 28 producer input/dependency hashes were also checked. The sealed previous `chain_frontier_review/SHA256SUMS.json` and every entry in it, all 26 old sealed physical-input hashes, and the prior analytic-source hashes were verified before any acceptance. `INHERITED_PROVENANCE.json` records these inherited checks. The independent kernel is pinned to

30c997e6e56135af60cd989ab22e31a8957346dc3ff2235ae8ac6b2c62916a19.

The shared working tree is an extracted checkpoint without Git metadata. No commit or remote publication is inferred from this review.

## 2. Small-patch physical input and complete trace upper bound

The independent physical kernel reconstructs the spin-one dimer basis from integer columns in the physical product-spin basis. Its diagonal Gram weights are

(3,2,2,2,1,2,6,2,1),

and strong-dimer excitation energies are 0,1,3 with multiplicities 1,3,5. The physical spin raising/lowering factors and the usual Heisenberg 1/2 factor are accounted for exactly. No normalized-basis square roots are approximated.

At M=4 and g=.1625/.175, the complete previously audited ground inputs are reused only after their exact record and integer-vector hashes match. Their prior review includes the entire H-applied support and full residual. At g=.1615 and the g=.2 diagnostic, the small-patch input is rebuilt anew: physical Hamiltonian action on every reached configuration, exact metric Rayleigh quotient, entire residual square, local 81-dimensional PSD, full-space cutoff, and Temple interval all agree with the saved records.

Write h_i = S_(i,0) dot S_(i,1)+2. The local bound

g V + a(h_i+h_j)+b I > 0

gives alpha=1-2a>0 and

H_M >= -2M + alpha sum_i h_i - M b.

The full reference multiplicities are the coefficients of (1+3x+5x^3)^M. In particular, all 9^4=6561 states are counted at M=4, the reference ground has multiplicity one, and the first excited bin has multiplicity 12. Thus the second physical eigenvalue is at least c_4=-8+alpha-4b. With rho_4<c_4, the full-space unique ground satisfies

e_- = rho_4 - R_4^2/(c_4-rho_4) <= E0(4) <= rho_4.

For t>0, put Q_4(t)=exp(t rho_4) Z_4(t). The resulting complete trace upper bound is

Q_4(t) <= exp[t(rho_4-e_-)]
 + exp[-t(-8-4b-rho_4)] [(1+3exp(-alpha t)+5exp(-3alpha t))^4-1].

Only the unique lowest reference level is removed by the subtraction. Every other physical level is controlled by the ordered min-max comparison, across the full Hilbert space.

## 3. The largest input is genuinely Rayleigh-only

At M=8 the independent audit reconstructs the exact metric Rayleigh quotient directly from the saved integer vector. It uses the independently derived unit weak-bond kernel and the correct periodic edge multiset. The vector has one trial-state coefficient array supported on 43,294 basis configurations, inside full dimension 9^8=43,046,721 (16 physical spins). The support dimension is neither a retained-band count nor an MPS bond dimension.

Only matrix elements returning to the trial support enter v*Hv. Omitting outside-support components here is exact because the bra is zero there; no residual statement is inferred. The resulting affine expectation <H0>+g<V_unit> reproduces each saved largest Rayleigh quotient. No largest residual, energy lower endpoint, spectral isolation, local comparison, thermal upper bound, or retained-band completeness is used. This includes the g=.2 diagnostic, whose old largest Temple certificate fails.

For any nonzero trial, the variational principle alone gives

Z_8(t) >= exp(-t rho_8).

Let delta=rho_8-2rho_4. The only largest-containing ratios required by the new cycle are

J = Z_8(2 beta)/Z_4(beta)^4
  >= exp(-2 beta delta)/Q_4^+(beta)^4,

C = Z_8(2 beta)/Z_4(2 beta)^2
  >= exp(-2 beta delta)/Q_4^+(2 beta)^2.

The audit function accepts the largest energy as a single rational scalar. Source geometry and trial normalization are separately verified; they do not introduce additional largest spectral premises. The producer's minimal/full/poisoned-record equality test agrees with this analytic and independent implementation dependency.

## 4. Time-first purification, basepoints, and adjacent swap

Let v=(n,beta), n=4; D_x and D_t double cell count and inverse temperature. Set

P_i(v)=Z(D_i v)/Z(v)^2.

At each even spatial size used here, spatial purity is the purity of the normalized nonnegative spectrum of an even power of the self-adjoint transfer operator. Thermal purity uses positive Gibbs weights. Both are at most one. The spatial transfer operator itself need not be positive. The self-adjoint transfer construction and all-integer trace identity are inherited from the same already-audited chain model.

For a normalized nonnegative spectrum with purity p, normalized squaring has purity at least

G(p)=1-(1-p)^2/(2p^2).

G is increasing on (0,1]. For the time-space staircase q1=P_t(v), q2=P_x(D_t v), exact cancellation gives

J=q1^2 q2=P_x(v)^2 P_t(D_x v), C=q2.

Since P_x(v)<=1, P_t(D_x v)>=J. Thermal squaring then gives

a=G(J) <= P_t(D_xD_t v).

Set w=D_xD_t v=(8,2 beta). A second exact identity gives

C^2 P_t(w) = P_t(D_t v)^2 P_x(D_t^2 v).

The first factor on the right is at most one; hence spatial squaring yields

b=G(C^2 a) <= P_x(D_t w).

Thus (a,b) is a time-space staircase based precisely at w. To convert it to the canonical space-time staircase, let c=P_x(w), e=P_t(D_x w). Commuting the doublings in the partition functions gives

e c^2 = P_t(w)^2 P_x(D_t w) >= a^2 b.

Because c,e<=1, independently valid canonical lower endpoints are

S=a sqrt(b) <= c, T=a^2 b <= e.

The base remains (M=8, 2 beta). No temperature coordinate has been silently relabeled as a spatial one. `PATH_LEDGER.json` records an independent symbolic monomial verification of all three identities with coordinate basepoints.

The rational program independently bounds the two small-patch traces, checks J and C, reconstructs a and b, verifies the saved 40-decimal square-root witness by integer squares, and reproduces the canonical downward-rounded pair. All 36 quarter-step rows across four couplings are replayed, not only the selected maxima.

## 5. Canonical continuation and all integer finite windows

Only after conversion does the canonical recursion apply:

S' >= G(S^2 T), T' >= G(T^2 S').

The audit reproduces every 12-decimal upward-rounded defect update. At the accepted common defect u<=1/100, the previously audited signed-transfer all-integer theorem gives

Delta_M >= log(1/(5u))/beta_final, for every integer M>=n_final.

For each saved rational gap d, acceptance is independently checked as

exp(beta_final d) 5u < 1,

using the review's exact Taylor/geometric-remainder exponential enclosure. No floating logarithm controls acceptance. The inherited scalar library's legacy text mentions even sizes; the all-integer conclusion here instead invokes the explicitly proved signed-transfer theorem.

Before asymptotic acceptance, the review uses the sharp signed-transfer finite-window lemma. For S,T>0 and P=S^2T>1/2, define

w=(1+sqrt(2P-1))/2, r=(1-w)/w, D=T/(1+r^2),

I=(1-r) min(S sqrt(D),D).

Every integer n<=M<=2n then has thermal purity at least I at the same inverse temperature. The positive dominant transfer eigenvalue is identified from positivity of all physical odd traces, and the remaining signed spectrum is bounded by its absolute tail. Thus the interpolation does not assume all transfer eigenvalues are positive.

This audit reconstructs the roots at 60 decimal places and verifies each saved lower purity. Every gap endpoint d passes exp(beta d)(1-I_saved)<I_saved. The required windows are contiguous:

| g | Window | Gap lower bound |
|---|---|---:|
| .1615 | [8,16] | .049448541150 |
| .1615 | [16,32] | .045503248236 |
| .1625 | [8,16] | .046962483671 |
| .1625 | [16,32] | .043184410634 |
| .175 | [8,16] | .014052800685 |
| .175 | [16,32] | .009982424354 |
| .175 | [32,64] | .008408773050 |
| .175 | [64,128] | .007962629969 |

All exceed their corresponding selected asymptotic gap.

## 6. New exact short-size bridges, M=2,...,7

The three new local certificates are rebuilt independently as weighted rational symmetric 81×81 matrices. Exact LDL elimination in all nine magnetization blocks yields 81 strictly positive pivots for each certificate. The stored producer inertia is not used as proof.

| g | a | b |
|---|---|---|
| .1615 | 6/25 | 14943794857/200000000000 |
| .1625 | 6/25 | 75602729373/1000000000000 |
| .175 | 13/50 | 40491147803/500000000000 |

Each local inequality sums to the complete-space cutoff

lambda_2(H_M) >= c_M=-2M+(1-2a)-Mb,

for every M>=2, with both M=2 weak edges retained. Whenever a trial quotient rho_M<c_M, min-max and variationality give finite-volume uniqueness and Delta_M>=c_M-rho_M. No residual is needed for this short-size use.

For M=2,...,6 the trial is normally the singlet product, whose quotient is exactly -2M. Its spin expectations vanish, so weak-edge expectations vanish even with the periodic multiplicity convention.

At M=7, all three couplings use the **same saved 365-support integer vector**, originally proposed at g=129/800. Its exact norm and affine expectation are independently reconstructed:

norm = 676843716479289704148122780670,

<H0> = -173851172623999220440039979477/12534142897764624150891162605,

<V_unit> = -19879453941458532186392701032/12534142897764624150891162605.

Each new quotient is this exact affine polynomial evaluated at its new g. The original g=129/800 quotient also agrees as a consistency check. No optimality or new eigenvector claim is made.

At g=.175, M=6 needs the saved 2,434-support depth-three trial instead of the singlet product. The independent unit-coupling kernel reconstruction reproduces its exact quotient

rho_6 = -912079333106518505400235364286/75204857386585881711091256647.

All six short-size gaps are strictly positive. Their minima are .071686154290, .066383623762, and a rational number greater than .060886447122 respectively. Together with the windows and the asymptotic regime, they cover every integer M>=2 with no missing odd or short size.

## 7. Reproduction and audit files

Run `REPRODUCE.sh` from any directory. The audit imports no producer mathematical module and calls no eigensolver. It uses the pinned earlier independent physical/exponential kernel, newly written Rayleigh-only and path algebra, and independently reconstructed scalar/window bounds.

The process pins to one permitted CPU, sets BLAS/OpenMP threads to one, and has a 1 GiB address-space hard limit, below the requested 1.5 GiB ceiling. Full final runtime/RSS and exact verifier hash are in `SUMMARY.json`; the final complete replay took 17.61 seconds and 37.73 MiB peak RSS. Verification cost is distinct from the original trial-search cost.

- `SUMMARY.json`: accepted scope, gaps, resource limits, and producer/verifier hashes
- `review_g*.json`: complete exact arithmetic checks, all beta rows, local LDL pivots, affine trials, all windows, and short-size cutoffs
- `PATH_LEDGER.json`: independent symbolic partition-function identities and basepoints
- `INHERITED_PROVENANCE.json`: verified prior audit, physical inputs, and analytic sources
- `INPUT_SHA256SUMS.json`: observed and checked input hashes
- `PRODUCER_FROZEN_MANIFEST.json`, `snapshot/`: immutable reviewed producer bytes
- `verify_temperature.py`, `audit.log`: independent executable replay and completion log
- `SHA256SUMS.json`: final sealed review artifacts, excluding that manifest itself

The g=.2 record certifies only that the nine tested beta values 22,22.25,...,24 do not furnish accepted candidates. It does not exclude other temperatures, adaptive orders, stronger inequalities, or the physical model's gap.
