# Independent audit of the continuous fully frustrated perturbation extension

Updated: 10 October 2026, 14:01 EDT / 18:01 UTC.

## Verdict and precise statement

**PASS.** The six selected new closed parameter intervals, their complete physical
inputs, their scalar certificates and all missing integer sizes pass independent
exact reconstruction. The baseline interval was also replayed afresh. No gap in
parameter coverage or finite-size coverage was found.

For the periodic square spin-1/2 bilayer with unit rung exchange, crossed exchange
`J=3/10` and straight exchange `J+epsilon`, retain every positive-direction
periodic adjacency separately, including the parallel contributions for a
direction of length two. For every integer square side `L>=2` and every
`0<=epsilon<=171/20000`, the finite-volume ground state is unique and

    Delta_L >= 130756138215761138933052179454005525
               / 170141183460469231731687303715884105728
            > 0.000768515509.

On the smaller closed interval `0<=epsilon<=17/2000`, the stronger common bound is

    Delta_L >= 579534716789337058753503842495191995
               / 340282366920938463463374607431768211456
            > 0.001703099464.

These are sufficient uniform certificates, not estimates of the actual gap or
of a maximal certifiable parameter. The result is for square tori. It makes no
arbitrary-aspect-ratio assertion. No conclusion above `epsilon=0.00855` follows
from the unsuccessful proposal grids.

The review imports **no producer code and no project arithmetic modules**.
`audit_interval.py` reconstructs all physical and scalar quantities using Python
integers and `Fraction`; NumPy only reads the saved integer trial-vector files.
The analytic thermal-transfer theorem and its hypotheses remain the previously
audited mathematical foundation, rather than being reproved from microscopic
Trotterization in this review.

## 1. Audited intervals and both kinds of coverage

| Closed epsilon interval | Fixed vector epsilon | Initial beta | Asymptotic entry side | Strict decimal gap bound | Minimum finite-window gap |
| --- | --- | --- | --- | --- | --- |
| [0, 0.00475] | Vacuum | 28.5 | 32 | 0.008090283176 | Separate short-size bridge: 0.343 |
| [0.00475, 0.006] | 0.006 | 30.5 | 16 | 0.026872599723 | 0.037130918004 |
| [0.006, 0.0075] | 0.0075 | 31.5 | 32 | 0.009589950085 | 0.014610346197 |
| [0.0075, 0.008] | 0.008 | 32 | 32 | 0.007867831452 | 0.012731595575 |
| [0.008, 0.00825] | 0.008 | 32.5 | 64 | 0.005936012610 | 0.008455332887 |
| [0.00825, 0.0085] | 0.0085 | 32.5 | 128 | 0.001703099464 | 0.002919360355 |
| [0.0085, 0.00855] | 0.0085 | 32.5 | 256 | 0.000768515509 | 0.001370774759 |

The exact parameter boundaries are

    0, 19/4000, 3/500, 3/400, 1/125, 33/4000, 17/2000, 171/20000.

Every endpoint equals the next interval's beginning exactly. All intervals are
closed and each proof uses its entire interval, so these seven pieces cover the
whole claimed continuum without extrapolation from a grid.

For the six new pieces, the replay checks respectively 3, 4, 4, 5, 6 and 7
finite-size windows. Each starts at `n=2` and covers every integer side in
`[n,2n]`, including odd sides. Consecutive windows share their endpoints and the
last reaches the asymptotic entry side. All 29 window gaps are strictly larger
than their interval's asymptotic gap, so the latter controls the uniform bound.

## 2. Fresh physical kernels and full-action polynomials

The vector artifacts use the orthogonal rational rung columns

    (0,-1,1,0), (1,0,0,0), (0,1,1,0), (0,0,0,1),

with metric weights `(2,1,2,1)`. Direct two-spin physical matrices verify that the
first column has rung energy `-3/4` and the other three have energy `1/4`.
For each inter-rung physical exchange, the checker builds the full 16 by 16
physical-spin matrix, transforms its action into these exact columns and
verifies reconstruction of every physical output component. The Hamiltonian
normalization and basis convention are therefore checked rather than inferred
from the saved Rayleigh quotients.

For each geometry, the checker independently generates the two positive spatial
directions and combines parallel edges into weights `w_ij`. It verifies weighted
degree four and total edge weight `2N`. It then constructs both `H_FF psi` and
`V psi`, with `H(epsilon)=H_FF+epsilon V`, on **all** rung configurations reached
by their full action. Outputs are never projected back into the trial space.
Python integers prevent fixed-width overflow in the large saved amplitudes.

The exact contractions are

    rho_0 = <psi,H_FF psi>/<psi,psi>,
    rho_1 = <psi,V psi>/<psi,psi>,
    m_0   = <H_FF psi,H_FF psi>/<psi,psi>,
    m_1   = 2<H_FF psi,V psi>/<psi,psi>,
    m_2   = <V psi,V psi>/<psi,psi>.

Consequently

    rho(e) = rho_0 + rho_1 e,
    R(e) = (m_0-rho_0^2)
         + (m_1-2 rho_0 rho_1)e
         + (m_2-rho_1^2)e^2.

All 12 distinct geometry/center polynomial sets reproduce the stored
coefficients, full metric norms and saved-point exact Rayleigh quotients and
full residuals. The checker additionally verifies the positive-semidefinite
2 by 2 covariance condition for `(H_FF,V)`, including `R_2>=0`.

The full Hilbert dimensions are `256`, `65,536` and `4,294,967,296`; the fixed
linear trial dimensions are `23`, `93` and `377`. One vector per geometry is
retained, at each chosen center. The full action unions have `58`, `1,301` and
`21,345` configurations. These union dimensions do not replace full-spectrum
control. The representation is a sparse rational Ritz vector, not an MPS; no
MPS bond dimension is assigned.

Since `rho` is affine and `R` is convex, over `I=[l,h]` their upper bounds are
exactly bounded by the larger endpoint value. Thus no interior parameter sample
is needed and there is no missing residual extremum between samples.

## 3. One fixed reference across each closed interval

For each saved rational `a>=0,b>0`, the checker directly reconstructs

    M(e) = e v_ij + a(P_i+P_j) + b I

in the 16-dimensional physical-spin basis. A separate rational LDL recurrence
checks positive pivots at **both** interval endpoints. These pivots also match
the stored witnesses. As `M` is affine, its entire closed interval is positive.
The reference parameters are fixed on the interval; separately optimized
endpoint parameters are never interpolated.

The weighted-star inequality is valid with parallel edges. For an occupied
triplet set `A`, each central triplet and its occupied neighbors give

    T_i . sum_j w_ij T_j >= -sum_j w_ij - max_j w_ij.

For equal weights this follows from angular-momentum addition; for unequal
weights it follows by decomposing weights into nested level sets. Summing stars
counts every active edge twice and yields

    f(A) = |A| - (3/10)(E(A) + (1/2) sum_i m_i(A)).

The independent checker enumerates all `2^N` occupied subsets directly by
bitmask, recomputing active edge weights and maximal incident weights. Each set
has rank `3^|A|`; for each `q` the ranks sum to `binomial(N,q)3^q`, and their total
is `4^N`. Every saved energy/multiplicity bin is reproduced.

Summing the local comparison, with weighted degree four, gives

    H(e)-E00 >= D_a-B,
    D_a(A)=f(A)-4a|A|, B=2Nb, E00=-3N/4.

The vacuum block has rank one and value zero in `D_a`; all nonvacuum values are
strictly positive. Ordered min-max therefore bounds the physical second
energy by the same fixed number

    alpha = E00 + min_{A nonempty} D_a(A) - B.

This bounds the entire spectrum in order. The perturbation need not preserve
triplet occupancy. Every interval satisfies `alpha>rho_max`. Its ground state
is unique and Temple's inequality gives, throughout the interval,

    rho(e)-delta <= E_0(e) <= rho(e),
    delta = R_max/(alpha-rho_max).

All endpoint maxima, `alpha` and `delta` are independently reproduced as exact
fractions. Crucially, only the correction is made uniform; the center remains
the exact affine function `rho(e)`.

## 4. Uniform complete heat tails and correlated energy factors

Separating the single ground state from the ordered nonvacuum reference levels
gives, for each seed geometry,

    exp(beta rho(e)) Z(beta,e)
      <= exp(beta delta)
       + sum_(q,f),q>0 multiplicity(q,f)
         exp[-beta(E00+f-4aq-B-rho(e))]
      <= Q(beta).

Replacing `rho(e)` by its maximum only in the tail gives a valid upper bound
`Q`; the ground contribution is `exp(beta delta)`. Every one of the `4^N-1`
excited reference levels is counted. There is no unbounded omitted low band.
The variational ground upper bound also implies
`exp(beta rho(e)) Z(beta,e)>=1` for every positive temperature.

Writing the three seed Rayleigh functions as `rho_0,rho_1,rho_2`, the checker
forms the four affine combinations before taking endpoint maxima:

    rho_1-2rho_0,
    rho_2-2rho_1,
    2rho_2-8rho_0,
    4rho_2-8rho_1.

The volume-proportional rung energies cancel exactly. The maximum of each
combined affine function is checked directly against the saved rational value.
This retains the correlation between energy shifts; substituting separate
maxima for its terms would be a different, weaker argument.

The initial lower inputs are

    A >= exp(-beta M_A)/Q_0^2,
    B >= exp(-beta M_B)/Q_1^2,
    C >= 1/Q_2^2,
    J1 >= exp(-beta M_J1)/Q_0^8,
    J2 >= exp(-beta M_J2)/Q_1^8.

In particular the exact identities `J1=A^4 B^2 C` and `J2=B^4 C^2` cancel the
unneeded partition factors before taking bounds. They justify the correlated
first updates and do not assume independence of the seed traces.

The fresh exponential routine uses 224-bit outward dyadic rounding, reduction
to `[0,1/8]`, 64 Taylor terms and the rigorous tail bound

    first_omitted_term / (1-reduced_argument/66).

It handles negative arguments by reciprocal enclosures and then squares with
outward rounding. It is distinct from both the producer's 128-bit routine and
the earlier 192-bit verifier. All stored trace upper bounds dominate these new
independent upper bounds. All five stored lower inputs lie below the new
independent lower bounds. Floating proposal scans and displayed decimals are
not used for acceptance.

## 5. Exact bootstrap and every integer finite window

With `G(x)=1-(1/x-1)^2/2`, the checker independently replays the first updates

    A1=G(J1), B1=G(J2 A1), C1=G(C^4 A1^2 B1)

and all subsequent three-step cycles, rounding each update down to a 128-bit
dyadic exactly. Every stored state, defect, temperature, side, round count and
accepted state matches. The accepted common defects obey the original
`u<=1/500` threshold, so this review does not require the later enlarged
`1/200` acceptance domain. Every asymptotic gap is validated by the outward
inequality

    exp(beta_final gap) < 1/(32u).

For finite windows, this review checks the signed-transfer lemma's use and
independently implements it without importing `finite_window_2d.py`. Given
`p=S^2 T>1/2`, put

    w=(1+sqrt(2p-1))/2, r=(1-w)/w, D=T/(1+r^2),
    I(S,T)=(1-r) min(S sqrt(D),D).

The inverse-purity bound supplies the unique largest-modulus transfer weight.
Its transfer eigenvalue is positive: otherwise all sufficiently large odd
physical traces would be negative. The signed-tail estimate applies to every
integer length, and absolute-spectrum interpolation at the two even endpoints
gives `T(L,beta)>=I(S,T)` for every integer `n<=L<=2n`.

For the two-dimensional staircase, the transverse spatial estimate gives
`S_*=A^2 sqrt(2B-1)`, the first thermal interpolation gives `T_*=I(B,C)`, and the
second gives `C_*=I(S_*,T_*)`. The spatial estimate is uniform across the finite
window because `c^s-d^s`, for `0<=d<c<=1` and `1<=s<=2`, has no interior minimum.
The monotonicity of these expressions in their supplied lower inputs makes
outward square-root rounding safe.

Every inverse-purity condition is checked exactly. Every 40-decimal square-root
lower endpoint is independently verified by its two bracketing integer squares.
Every saved finite-window purity is exactly reproduced. Each exceeds `1/2`, and
the saved gap is then validated against the fresh exponential enclosure:

    exp(beta gap)(1-C_*) < C_*.

The physical transfer hypotheses hold at every parameter in these intervals:
the layer coupling eigenvalues are `epsilon` and `2J+epsilon`, both nonnegative,
and the audited rung real structure and periodic multiplicity convention are
unchanged. Nothing singular is assumed at the zero endpoint of the baseline.

## 6. Fresh replay of the baseline interval

To avoid relying only on the prior report, the checker reconstructs the complete
vacuum action for all three seed geometries. It obtains `rho=E00` and

    R(e)=(3/4)e^2 sum_(i,j) w_ij^2,

with coefficients `12,18,24`. It repeats the baseline reference histograms, both
PSD endpoints, Temple intervals, fresh 224-bit heat bounds, exact recurrence and
final gap test.

The baseline's separate short-size bridge is also replayed. The `L>=4` square
graphs are simple and triangle-free, including odd `L>=5`. For occupied size
`q`, the active-edge bound is `min(2q,floor(q^2/4))`. Its eight-level cutoff,
monotone continuation for `q>=8`, fixed local comparison, and special `L=2,3`
perturbation estimates give a minimum of `343/1000` through `L=31`. This exceeds
the baseline thermal bound at all `L>=32`.

Thus both the inherited parameter piece and every new piece have been checked
in this single reproducible audit, including their different finite-size bridges.

## 7. Reproduction, provenance and limits

From the repository root:

    PYTHONDONTWRITEBYTECODE=1 python research_20261010/epsilon_interval_review/audit_interval.py

The checker reads only immutable inputs and writes `audit_results.json` in this
review directory. `REPRODUCE.sh` also saves the console output as `audit.log`.
BLAS/OMP/MKL thread counts are fixed at one. A complete replay used about 22
seconds and about 44 MiB peak RSS; exact measured values for the final run are
stored in `audit_results.json`.

The machine-readable result contains the exact complete coefficients, all finite
window witnesses, final rational bounds, resource measurements and SHA-256
hashes for 37 reviewed source/input files. Repeated reads reject a changed input,
and every recorded input hash is checked again at completion. The local
manifest covers the independent checker, report and outputs.

The supplied tree has no Git metadata. `git status` and `git rev-parse HEAD`
therefore could not verify a checkout branch or commit; the reviewed contents
are identified by hashes. The root README names source commit
`6be889a30f642bde77fb89af75b3a7379615bed1`, but this audit does not claim to have
verified that checkout identity. No original record, producer code, baseline
file or remote state was changed. All new files are confined to this directory.

The unselected initial unsplit interval and failed proposals are outside this
review's acceptance set. The six selected intervals suffice for both reported
unions. There were no new eigensolves, full many-body diagonalizations, parameter
grid inferences or claims of maximality.
