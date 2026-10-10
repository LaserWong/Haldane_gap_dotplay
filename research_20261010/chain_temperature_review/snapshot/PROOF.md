# Temperature-first chain bootstrap with Rayleigh-only largest input

Updated 10 October 2026, 14:42 America/New_York (EDT) / 18:42 UTC.

**Status: exact-arithmetic producer candidates, pending independent review.** The analytic formulas below were checked separately by the reduced-input-bootstrap worker, but that does not replace an independent physical/arithmetic review of these files. No new many-body eigensolver was run. Existing ground trial vectors and bounds are reused.

## 1. Model, units, dimensions, and scope

For integer M >= 2, the periodic spin-one alternating chain is

H_M(g) = sum_i S_(i,0) dot S_(i,1) + g sum_i S_(i-1,1) dot S_(i,0).

The strong exchange is one. There are M two-spin cells, 2M physical spins, and full Hilbert dimension 9^M. The physical exchange pattern has period two in microscopic sites and period one in cells. Both periodic weak edges are retained at M=2; no simple-graph edge deduplication is made. Only cell counts are doubled or interpolated here. The inherited self-adjoint spatial transfer construction and cell/time-reversal hypotheses are those already audited for this same chain in `../chain_audit/CHAIN_CERTIFICATE_PROOF.md` and `../chain_frontier_review/FRONTIER_PROOF.md`.

The seed uses n=4 and 2n=8 cells, with full dimensions 6561 and 43,046,721. The saved depth-four n=8 trial has linear support dimension 43,294. Only its Rayleigh quotient is needed here, not its full residual support or isolation. These are not MPS bond dimensions.

The resulting candidates concern **every integer M >= 2**, including odd cell counts. They prove finite-volume uniqueness if their inputs and arithmetic pass independent review. They do not identify a physical transition or a maximal certifiable coupling.

## 2. Exact-input contract

Let rho_M be the Rayleigh quotient of any nonzero saved vector. Variationality alone gives E0(M) <= rho_M, hence

Z_M(t) >= exp(-t rho_M), t > 0.

No residual, spectral isolation, uniqueness, or completeness assumption is needed for this lower bound. In particular, an input rejected by a Temple ground-isolation test still supplies this valid trace lower bound.

For M=4 only, use the existing ground enclosure [e_-,rho_4] and full independent-dimer bin comparison

H_4 >= -8 + alpha sum_i h_i - B,

with h_i eigenvalues 0,1,3 of multiplicities 1,3,5. Then Q_4(t)=exp(t rho_4)Z_4(t) obeys

Q_4(t) <= exp[t(rho_4-e_-)]
          + exp[-t(-8-B-rho_4)] ((1+3exp(-alpha t)+5exp(-3alpha t))^4-1).

The full bin count and unique-ground Temple premises are required at this smaller patch. Existing frontier records supply them; this package does not infer spectral completeness from a small residual.

Set delta=rho_8-2rho_4. The only trace combinations needed are

J = Z_8(2 beta)/Z_4(beta)^4
  >= exp(-2 beta delta)/(Q_4^+(beta))^4,

C = Z_8(2 beta)/Z_4(2 beta)^2
  >= exp(-2 beta delta)/(Q_4^+(2 beta))^2.

The largest-input schema therefore contains exactly one energy field: `exact_rayleigh`. The file `certify.py` computes the identical cycle from (a) that one-field dictionary, (b) the entire historical ground record, and (c) a dictionary whose unused large-patch ground bounds, residual, cutoff, local form, size, and status fields are poisoned with unusable strings. The exact equality is asserted and recorded for every tested coupling. This verifies the implementation dependency, not the physical correctness of the supplied Rayleigh quotient.

At g=1/5, the saved n=8 Temple cutoff fails, but the reduced-input cycle still evaluates. Its bounded tested candidates fail later at the scalar stage. The failed old isolation is therefore demonstrably no longer an input blocker.

## 3. Time-first cycle and canonical conversion

Let v=(n,beta), with D_x doubling cells and D_t doubling inverse temperature. Define

P_x(v)=Z(D_x v)/Z(v)^2, P_t(v)=Z(D_t v)/Z(v)^2.

At the even cell sizes in the staircase, each lies in (0,1]. Thermal purity uses positive Gibbs weights. Spatial purity uses an even power of a self-adjoint transfer operator; this does not assume that all transfer eigenvalues are nonnegative.

For any purity p, normalized squaring gives the increasing lower bound

G(p)=1-(1-p)^2/(2p^2).

In the time-then-space staircase, q1=P_t(v), q2=P_x(D_t v). Exact cancellation gives J=q1^2 q2 and C=q2. A square identity first gives

P_t(D_x v) = q1^2 q2/P_x(v)^2 >= J.

Thermal squaring therefore proves

a = G(J) <= P_t(D_t D_x v).

At w=D_t v, the same square identity gives

P_x(D_t w) = P_t(D_x w) P_x(w)^2/P_t(w)^2 >= a C^2.

Spatial squaring then proves

b = G(C^2 a) <= P_x(D_x D_t^2 v).

Thus (a,b) is a **time,space staircase based at v2=(2n,2 beta)**. Its two entries are respectively P_t(v2) and P_x(D_t v2). It is not yet a canonical space,time pair.

For the canonical pair c=P_x(v2), e=P_t(D_x v2), cancellation gives

e c^2 = P_x(D_t v2) P_t(v2)^2 >= b a^2.

Since c,e <= 1, this yields the rigorous adjacent-swap conversion

S = a sqrt(b) <= c, T = a^2 b <= e.

The base remains exactly v2. All subsequent recursion and interpolation are canonical; no spatial direction is silently exchanged with physical time.

Every formula is used only while its lower arguments are positive. `certify.py` rounds every scalar lower endpoint down to 12 decimal places, with an exact 40-decimal integer-square-root enclosure for sqrt(b). Exponential intervals use the existing rational 128-bit kernel. Downward rounding preserves all lower-bound directions.

## 4. Canonical continuation and finite windows

From the canonical pair at n=8, beta'=2 beta, the already-audited sequential recursion is

S' >= G(S^2 T), T' >= G(T^2 S').

It doubles n and beta' together. The saved exact replay accepts once u=max(1-S,1-T)<=1/100. The inherited signed-transfer all-integer interpolation gives

Delta_M >= log(1/(5u))/beta_final, every integer M>=n_final.

The producer supplies a rational lower endpoint from a positive rational logarithm series. The legacy scalar library text mentions even sizes; the all-integer scope used here explicitly comes from the later reviewed signed-transfer theorem, not that legacy label.

For each missing dyadic window n<=M<=2n, use the independently reviewed finite-window lemma. With P=S^2 T>1/2,

w=(1+sqrt(2P-1))/2, r=(1-w)/w, D=T/(1+r^2),

C_window=(1-r) min(S sqrt(D),D).

It supplies T(M,beta')>=C_window for **every integer** in that window. The candidate gap d is checked by a rational exponential upper enclosure satisfying exp(beta' d)(1-C_window)<C_window. The generated windows are contiguous from M=8 to n_final.

## 5. All short integer sizes without new many-body diagonalization

For each coupling, the producer optimizes an 81-dimensional local proposal and checks exact rational positive definiteness of

g V + a(h_i+h_j)+b I > 0.

The resulting alpha=1-2a gives, simultaneously for 2<=M<=7,

lambda_2(H_M) >= c_M=-2M+alpha-Mb.

The subscript 2 denotes the second ordered eigenvalue, counting multiplicity. If any normalized trial has quotient rho_M<c_M, then the first eigenvalue is unique and

Delta_M=lambda_2-lambda_1 >= c_M-rho_M.

This lower-bound direction uses only lambda_1<=rho_M. Full residual or Temple isolation is unnecessary for these short-size trial upper bounds too.

For M=2,...,6, the trial is normally the dimer-singlet product, with exact quotient -2M. At g=.175 and M=6, reuse the existing quotient from `../chain_frontier/chain_s1_M6_g7d40_depth3_ground.json` instead; its exact source hash is recorded with the row and in `INPUT_SHA256.json`.

For M=7 at all three successful couplings, reuse the same fixed 365-dimensional integer vector from `../chain_frontier/chain_s1_M7_g129d800_depth2_trial.npz`. Its unnormalized dimer basis carries the positive product Gram metric from local weights (3,2,2,2,1,2,6,2,1). The producer reconstructs the exact norm, diagonal H0 expectation, and expectation of the **unit-coupling** periodic weak-edge sum. Hence

rho_7(g)=<H0>_v + g <V_unit>_v

is exact for the entire new coupling evaluation; there is no assertion that the vector is a new Ritz eigenvector. As a consistency check, at g=129/800 this affine quotient must equal the old saved exact quotient. Every norm and affine expectation, source path, and SHA-256 is persisted. The original n=7 Hamiltonian has seven weak edges, including its periodic closing edge. Only PHP matrix entries are needed for the Rayleigh expectation; omitted H-action components cannot contribute because the trial is zero there.

## 6. Candidate values and complete coverage

| g | Initial beta | Canonical asymptotic onset M | All M>=2 gap candidate | Minimum short bridge |
|---|---:|---:|---:|---:|
| 323/2000 = .1615 | 39/2 | 32 | .039815121561 | .071686154290 |
| 13/80 = .1625 | 81/4 | 32 | .037716426713 | .066383623762 |
| 7/40 = .175 | 23 | 128 | .006791087005 | >.060886447122 |

Finite windows, each above its row's final all-size candidate:

- g=.1615: [8,16] .049448541150; [16,32] .045503248236.
- g=.1625: [8,16] .046962483671; [16,32] .043184410634.
- g=.175: [8,16] .014052800685; [16,32] .009982424354; [32,64] .008408773050; [64,128] .007962629969.

Each row is therefore a producer all-integer candidate with no missing small or odd size. The required new independent audit must check the input hashes, physical small-patch trace premise, largest Rayleigh quotient, new local comparisons, M7 affine expectation, M6 quotient, directed scalar arithmetic, and every bridge.

## 7. Comparison with the older obstruction and g=.2 diagnostic

The old all-beta obstructions at .1615, .1625, and .175 remain correct for their stated ground-only numerator, dimer-tail, **space-first canonical** recipe. That recipe requires an n=8 trace upper bound and suffers from its full tail. The present time-first recipe uses upper traces only at n=4, and its later adjacent-swap conversion preserves valid canonical basepoints. It is outside the older exclusion's explicitly limited order/input scope.

The bounded floating diagnostic tested beta=1,1.25,...,160 at four couplings. It found successful scalar temperatures for the first three, and none at .2. The exact producer rechecks nine quarter-step temperatures around each successful proposal; at .2 it checks beta=22,...,24 in quarter steps and obtains no candidate. These are finite-grid diagnostics, **not** all-beta obstructions, optimized local-parameter obstructions, physical gaplessness results, or maximal-coupling claims. No further coupling scan is included before independent review.

## Reproduction and integrity

Run `REPRODUCE.sh` from any directory. The finite exact producer took about five seconds and less than 83 MiB RSS in this executor. Both scripts pin to one permitted CPU and set BLAS/OpenMP threads to one; the address-space cap is 1500 MiB, below 1.5 GiB. The only eigenvalue proposal is for the local 81-dimensional comparison; no many-body eigensolver is invoked. All writes remain inside this new directory. The shared snapshot has no Git metadata, and no commit or remote publication is implied.

`INPUT_SHA256.json` hashes all consumed existing data, code dependencies, and inherited proof references. `FROZEN_MANIFEST.json` seals this producer package before independent review. Reproduction changes only local generated outputs and logs; auditors should snapshot the frozen bytes first.
