# Joint-purity and repeated-temperature chain extension

Updated 2026-10-10 15:19 America/New_York (EDT) / 19:19 UTC.

Status: exact-arithmetic producer candidates, with a separately implemented local verifier. External independent review is still required before promotion.

## Model and unchanged normalization

For every integer M >= 2, the physical Hamiltonian is

H_M(g) = sum_i S_(i,0) dot S_(i,1) + g sum_i S_(i-1,1) dot S_(i,0),

with physical spin one, unit strong exchange, and periodic cell labels. There are 2M spins and Hilbert dimension 9^M. The oriented weak-edge multiset has exactly M entries, including both distinct weak bonds at M=2. No deduplication occurs. The rational dimer basis is the previously independently reconstructed physical basis, with Gram weights (3,2,2,2,1,2,6,2,1) and strong excitation energies (0,1,1,1,3,3,3,3,3).

The active tree is an extracted checkpoint without Git metadata. This package changes no frozen prior source or record. Source hashes, rather than a new Git commit, identify its input bytes.

The exact all-integer M>=2 candidate bounds are:

| g | Gap lower endpoint | beta initial | Extra time-first / canonical cycles | Asymptotic onset M |
|---|---:|---:|---:|---:|
| .175 | .026579108896 | 22.2 | 3 / 1 | 128 |
| .18 | .013222512347 | 22.8 | 3 / 2 | 256 |
| .181 | .009728769181 | 23.1 | 3 / 2 | 256 |
| .182 | .005940278341 | 23.45 | 4 / 1 | 256 |

These four discrete couplings do not certify an interval between them.

## 1. Reusable joint trace identity

Let v be a space-temperature basepoint. Let D_x double the number of cells and D_t double inverse temperature, and define

P_i(v) = Z(D_i v) / Z(v)^2.

These operators commute. Exact cancellation, with no approximation or physical spectrum truncation, gives

P_x(v)^2 P_t(D_x v)
= Z(D_x D_t v) / Z(v)^4
= P_t(v)^2 P_x(D_t v).

Suppose a <= P_t(v) and b <= P_x(D_t v). At an even spatial basepoint both purities in either staircase are <= 1: the thermal spectrum is positive, and the spatial spectrum is the normalized nonnegative spectrum of an even power of the self-adjoint transfer operator. The underlying transfer operator may have negative eigenvalues.

Writing S_actual=P_x(v), T_actual=P_t(D_x v), and K=a^2 b, the same identity yields all three simultaneous lower bounds

S_actual >= sqrt(K),  T_actual >= K,  S_actual^2 T_actual >= K.

The last bound must be retained separately. Multiplying the two independent scalar endpoints would give only K^2 and discard valid information.

The purified-purity function is G(p)=1-(1-p)^2/(2p^2), monotone for 0<p<=1. Thus the next canonical spatial endpoint is

S_next >= G(K),

followed by T_next >= G(T_lower^2 S_next). This is the standard canonical update applied to a sharper valid lower bound on its joint input. After this first step the package conservatively uses the product of the new independent endpoints. No new canonical recursion theorem is assumed.

`verify_extension.py` checks the partition-function exponents and coordinate basepoints algebraically, reconstructs every new first canonical update, and checks every window separately.

## 2. Finite windows may use the same joint bound

The previously reviewed signed-transfer finite-window proof for every integer n <= M <= 2n uses the inverse-purity product P=S_actual^2 T_actual to bound the dominant weight. It does not require P's lower endpoint to equal the product of separately rounded bounds.

Given lower bounds S, T and a separate P_lower >= S^2 T, set

w = (1+sqrt(2 P_lower-1))/2,
r = (1-w)/w,
D = T/(1+r^2),
I = (1-r) min(S sqrt(D), D).

If P_lower>1/2, these imply thermal purity at least I on the whole integer window at the same inverse temperature. All functions are monotone in the required directions: a larger valid joint endpoint increases w, decreases r, increases D, and increases I. The proof is precisely the old signed-transfer proof with a sharper input to the dominant-weight estimate. The positivity of all physical odd traces selects the positive dominant transfer eigenvalue; positivity of the transfer operator is not assumed.

At a time-first state (a,b) the package supplies S <= a sqrt(b), T <= a^2 b and P_lower=a^2 b. At later canonical states it can use P_lower=S^2 T. Every saved square-root witness is downward rounded; every final I is downward rounded. Each positive gap d is accepted only after the exact exponential test

exp(beta d) (1-I) < I.

This joint-bound window step is essential at g=.18: using only the product of separately weakened endpoints fails the initial finite window even though the time-first recurrence can converge.

## 3. First time-space cycle and repeated cycles

The seed uses n=4 and inverse temperature beta. Let rho4 be the certified small-patch trial energy, rho8 any certified variational upper energy on M=8, and Q4(t)=exp(t rho4) Z4(t). The only required ratios involving M=8 are

J = Z8(2 beta)/Z4(beta)^4 >= exp[-2 beta (rho8-2rho4)] / Q4(beta)^4,
C = Z8(2 beta)/Z4(2 beta)^2 >= exp[-2 beta (rho8-2rho4)] / Q4(2 beta)^2.

The already reviewed time-first startup gives

a=G(J), b=G(C^2 a),

as endpoints for the time-space staircase based at exactly (M=8, inverse temperature=2 beta). The recurrence can be continued in the same order:

a_next=G(a^2 b), b_next=G(b^2 a_next).

Each such complete cycle doubles both cell count and inverse temperature. After k repeated time-first cycles the base is (8*2^k, 2 beta*2^k). At that very base the identity in Section 1 permits canonical conversion while retaining K=a^2 b. Each later canonical cycle again doubles both coordinates. There is no relabeling of time as space.

Every intermediate dyadic interval [n,2n] is certified by Section 2 before advancing. At any canonical endpoint with u=max(1-S,1-T)<=1/100, the previously audited all-integer signed-transfer theorem gives a gap d for every M>=n whenever

exp(beta_final d) 5u < 1.

The producer compares earlier and additional valid rounds rather than stopping at first threshold entry. Each tested endpoint is a separately valid candidate. An additional round need not improve the reported minimum; rounding and finite windows can dominate.

## 4. Physical data: no new large support or largest residual

The largest trial support is unchanged: 43,294 dimer configurations inside 9^8=43,046,721 physical states. The two saved M=8 integer vectors were originally proposed at g=.175 and .2 and have exactly the same basis support. This package reconstructs their exact two-by-two Gram matrix G, strong first moment K0, and weak first moment K1. Only matrix elements returning to the saved support contribute, which is exact for these expectations. No outside-support components are constructed, omitted as a claimed residual, or used to assert spectral completeness.

At each new g a two-dimensional floating generalized eigenproblem proposes integer combination coefficients c. The accepted energy is computed exactly as

rho8 = c^T (K0+g K1) c / (c^T G c).

The squared metric norm is checked positive. The two-dimensional combination search, the 43,294-dimensional configuration support, the full Hilbert dimension, and the one retained Rayleigh trial are different quantities. This is not an MPS calculation. No M=8 energy lower endpoint, residual, isolation condition, or complete trace upper bound is needed.

For M=4 the producer uses the existing depth-four recipe, with 1,099 trial configurations and all 1,107 configurations in the full H-applied support. New small-patch vectors are saved only for new couplings. The full physical space still has dimension 9^4=6,561. The separate verifier rebuilds their exact Rayleigh quotients and full residuals using the independently reconstructed physical kernel.

The local comparison gV+a(h_i+h_j)+bI>0 is checked by exact rational LDL in all magnetization blocks. It implies the full-spectrum comparison H4 >= -8 + alpha sum_i h_i - 4b, alpha=1-2a. The reference bins count every state via (1+3x+5x^3)^4. The full-space second-level cutoff and full residual give a Temple ground interval. The complete small-patch trace upper bound is exactly the one used in the prior reviewed temperature-first route, not a truncated trace.

## 5. Short sizes and complete coverage

A single independently checked local comparison at each g applies to all M=2,...,7. It gives lambda2(H_M) >= -2M+alpha-Mb. The M=2,...,5 trial is the singlet product with quotient -2M. The M=6 and M=7 trials are the previously saved 2,434-support and 365-support integer vectors. Their exact affine first moments are reconstructed at the new coupling; old quotients are not reused at the wrong g.

For each short size the cutoff minus the variational quotient is positive, proving uniqueness and the saved short-size gap. The six short sizes, all consecutive dyadic integer windows beginning at M=8, and the asymptotic all-integer theorem cover every integer M>=2, including odd M.

## 6. Residual-filter diagnostic and scope of the nonpasses

The saved M=8 ground records contain a complete residual square at g=.175 and .2. Thus a scalar residual-direction filter is available without a new third moment or state expansion. The universal physical upper bound H_M <= M(1+g)I gives R=8(1+g), and the admissible gain delta obeys

delta (R-rho8+delta) <= sigma^2.

Its optimal comparison gains are approximately 1.46e-7 at g=.175 and 5.70e-7 at g=.2. These are tiny compared with the curvature rho8-2rho4, approximately .00348783 and .00608196. The M=4 ground width at g=.2 is about 2.59e-9; tightening this endpoint alone is also negligible. The .2 residual is used here only for a saved-input diagnostic, not as an independently upgraded physical result in this package. New candidates above .175 use no largest residual.

The bounded floating search has no accepted route at .183, .184, .185, .19, .195 or .2. It is a search diagnostic, not an all-temperature or all-order exclusion, and says nothing about physical gaplessness. It uses beta=2,2.05,...,80 and at most seven additional time-first and seven canonical cycles. No monotonicity in g or continuous-coupling certificate is claimed.

## 7. Resources and next cheapest work

All executables pin to one permitted CPU, use one BLAS/OpenMP thread, and impose a 1 GiB address-space limit. Largest new arrays are the existing 43,294-support vectors; no 245,870- or 939,326-state residual support is reconstructed. The actual resource records are saved in `input_resources.json`, `summary.json`, and `verification.json`.

A next physical improvement should target the M=4 complete spectral tail or a different ratio/seed geometry. M=4 has only 6,561 physical states, with the largest total-magnetization block of size 1,107. Constructing its sparse full physical matrix or a modest low-band trial family should fit comfortably within this package's memory budget, but a rigorous global trace improvement requires certified omitted-state counting or validated full-block spectral enclosures. A new low Ritz value alone would not supply this. Such an extension is separate work; no large M=8 residual rebuild is justified by the tiny global-filter gain.

## Reproduction

Run `bash REPRODUCE.sh`. It rebuilds or validates the small saved artifacts, checks the two-trial first moments, repeats the bounded proposal search, generates exact candidate records, and runs the independent local verifier. Exact source hashes identify the external prerequisites. The old audited proofs provide the transfer construction, purification inequality, Temple theorem, and all-integer asymptotic theorem; the new contribution is the retained joint endpoint and its explicit use in both updates and windows.
