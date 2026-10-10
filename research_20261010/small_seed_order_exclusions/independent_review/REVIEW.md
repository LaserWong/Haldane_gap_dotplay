# Independent review: all six small-seed coordinate orders

## Verdict

**PASS.** For the ordinary spin-1/2 square bilayer at g=1/25 and g=1/20,
with unit rung coupling, equal straight in-layer couplings, no crossed
exchanges, and periodic positive-direction bond multiplicities, the specified
correlated cyclic lower-bound recipe fails for every finite real beta >= 0.
The seed family is 2x2, 4x2, 4x4 rungs, or its exact x/y image 2x2, 2x4, 4x4.
All six fixed orders are covered.

The maximum required failure indices are:

| g | xyt / yxt | xty / ytx | txy / tyx |
|---|---:|---:|---:|
| 1/25 | 4 | 3 | 3 |
| 1/20 | 2 | 2 | 2 |

This is a failure of the stated lower-bound algorithm even with exact
physical partition functions. It is not a failure of positivity of the
physical purities, physical gaplessness, a phase boundary, or a restriction on
larger seeds, new trace injections, improved inequalities, or arbitrary
adaptive order changes. The xty and txy routes do not reach a positive first
cycle to which the existing adjacent-swap transport recipe could be applied.

The new work is an analytic and independently implemented exact **scalar**
review. The physical complete-band and full-tail reconstruction is explicitly
inherited from the accepted review in `../../small_seed_exclusion_review`.
It is not rerun here, and no new physical vectors, spectral diagonalization,
or physical Hamiltonian moment calculation was performed.

## Provenance and independence

`INPUT_SHA256.json` records every dependency and verifies unchanged bytes at
both ends of the calculation. The three frozen scientific producer files are
checked against `../PRODUCER_FREEZE_SHA256.json`. The existing physical audit's
10-entry manifest, 43-entry source manifest, and 40 physical input hashes are
all checked. Overlapping entries are checked consistently. The accepted
physical result hash is

`6e78a354da036930520761566f0b255761b8baf6363e8caa6b2c3bb41ba77fa3`.

The reviewer imports no project code, including no producer scalar routine and
no prior exponential implementation. It reads the accepted rational physical
endpoints as data. The producer uses 256-bit/70-term rational exponentials;
this review independently implements 320-bit/84-term integer fixed-point
interval arithmetic. The review also independently reconstructs partition
monomials for all six orders and complete physical-spin edge multisets for
coordinate exchange.

The directory is an extracted shared snapshot without Git metadata. A local
write or passed hash check does not establish a new commit or publication.
Only this review directory was changed, and no remote write was made.

## Analytical checks

### Order-specific inputs and normalization

For v=(2,2,beta), let v1, v2, v3 be the successive coordinate doublings for an
order (i,j,k), and let q1, q2, q3 be their partition ratios. Exact cancellation
of formal partition-function monomials gives

- J1 = q1^4 q2^2 q3 = Z(v3)/Z(v)^8
- J2 = q2^4 q3^2 = Z(v3)^2/Z(v1)^8
- C0 = q3 = Z(v3)/Z(v2)^2

The independent symbolic ledger checks these statements for every permutation.
For xyt, the intermediate points are (4,2,beta), (4,4,beta). For xty they are
(4,2,beta), (4,2,2 beta). For txy they are (2,2,2 beta), (4,2,2 beta).
Thus the txy J2 denominator is Z4(2 beta)^8, and the xty/txy C0 denominator is
Z8(2 beta)^2. These cannot be obtained by permuting old numerical purity values.

Every input lies in (0,1], because each q is a genuine even-base spatial
transfer or Gibbs purity under the previously reviewed transfer assumptions.
The weighted products above justify clipping their upper bounds at one.

Writing ZN(beta)=exp(-beta EN) TN(beta), the physical exponential factors are,
respectively, 8E4-2E16, 8E8-4E16, 16E4-4E16, zero, and 4E8-2E16 for common J1,
spatial-first J2, time-first J2, time-last C0, and space-last C0. The restored
physical shift is checked as -3N/4. Retained multiplicities total 1+3N and all
upper-trace multiplicities total 4^N. These checks do not substitute for the
inherited physical endpoint and omitted-state acceptance.

### Upper propagation really excludes the specified recipe

For 0 < z <= 1,

G(z) = (z^2+2z-1)/(2z^2),    G'(z) = (1-z)/z^3 >= 0,    G(z) <= 1.

The first three outputs are G(J1), G(J2 a), G(C0^4 a^2 b), and subsequent
updates apply G to the ordered queue product a^4 b^2 c. While the exact recipe
has remained positive, the products are monotone in every nonnegative factor.
Upward interval propagation therefore dominates the exact-input recipe at
every visited step. A strictly negative propagated upper output proves that
the exact recipe either failed earlier or fails at this step. No negative
value is inserted into a later nonlinear product. Both independent replay and
saved-producer replay explicitly check the domain 0 < argument <= 1.

This is an upper enclosure of a *lower-bound recipe*, not an upper bound on
the physical purity itself.

### Hot interval

The independently checked monomial identity is

J1 = T4(beta)^4 P_x(2,2,2 beta)^2 P_y(4,2,2 beta) <= T4(beta)^4.

For the fixed 2x2 Hamiltonian, Gibbs purity is nondecreasing for beta >= 0:
its logarithmic derivative is 2(U_beta-U_(2 beta)) >= 0, since
U'_beta=-Var_beta(H) <= 0. Consequently J1 <= T4(4)^4 on [0,4]. Only Gibbs
purity is asserted monotone in temperature, not spatial purity.

The independently enclosed values of T4(4) are approximately 0.673621528 and
0.673030701 for g=1/25 and 1/20. Their exact rational fourth-power upper bounds
produce strictly negative first updates. These decimal values are diagnostic;
all acceptance uses the rational intervals in results.json. Beta=0 is covered.

### Every closed middle box

For each coupling and each of three representative orders, the code verifies
all 320 boxes [4+k/20,4+(k+1)/20], k=0,...,319. Exact endpoints, adjacency,
counts, and coverage of [4,20] are checked; these are uniform interval bounds,
not samples. Each exponential argument is ordered at its two endpoints before
applying monotonicity of exp. Numerators use upper bounds and denominators use
lower bounds, with doubled temperatures at the order-specific points.

For all 1,920 coupling/order/box combinations, the independently computed
upper inputs are no greater than the saved producer inputs, and independent
propagation gives a strictly negative witness. Separately, every saved
producer argument, every 256-bit upward-rounded output, its failure index,
and its negative witness are reconstructed exactly. Histograms match:

| g | Order | Fail 1 | Fail 2 | Fail 3 | Fail 4 |
|---|---|---:|---:|---:|---:|
| 1/25 | xyt | 18 | 150 | 70 | 82 |
| 1/25 | xty | 18 | 150 | 152 | 0 |
| 1/25 | txy | 18 | 225 | 77 | 0 |
| 1/20 | each representative | 149 | 171 | 0 | 0 |

The closest saved upper witnesses to zero remain below approximately
-0.0009107817 for g=1/25 xyt/xty, -0.0067434802 for g=1/25 txy, and
-0.0054346557 for all three g=1/20 representatives.

### Entire cold ray

The 4x4 upper trace is rebased on its accepted physical ground lower endpoint
E16-. Every retained and omitted-bin gap relative to that endpoint is checked
nonnegative. Hence its relative trace is bounded above by Urel(40) for
2 beta >= 40. Ground upper endpoints E4+, E8+ provide lower denominator
bounds by retaining the actual ground contribution.

The exact slopes are all positive:

- d1 = 2E16- - 8E4+
- dx = 4E16- - 8E8+
- dt = 4E16- - 16E4+ = 2d1

They give J1 <= exp(-20 d1) Urel(40), spatial-first J2 <=
exp(-20 dx) Urel(40)^2, and time-first J2 <= exp(-20 dt) Urel(40)^2 for the
entire beta >= 20 ray. With C0 <= 1 these fail by update two at g=1/25 and
update one at g=1/20. Positive slope signs, gap signs, relative trace bounds,
and every supplied cold witness all pass exact independent checks.

The hot interval, closed middle boxes, and cold ray cover every finite
beta >= 0 without a gap. Infinity is not treated as an evaluated Gibbs state.

### Exact extension from three to six orders

Relabel (x,y,layer) to (y,x,layer) on every physical spin. This is a tensor-factor
permutation and therefore a unitary. It preserves rung terms, exchanges
positive-direction x/y terms, and preserves periodic parallel multiplicities.
Since the two in-layer couplings are equal, the full Hamiltonians on nx by ny
and ny by nx are unitarily conjugate. Their partition functions agree at the
same beta. Applying this to the entire ordered path, with all basepoints,
proves xyt <-> yxt, xty <-> ytx, and txy <-> tyx.

The executable independently constructs both layers and rung bonds for all
seed shapes and their mirrors, and verifies the complete weighted edge
multiset equality. These finite graph checks supplement the general analytic
site-bijection proof; they are not a replacement for it. No time/spatial
unitary exchange is asserted.

## Independent exponential certification

The implementation reduces |z| by powers of two until y <= 1/8. Every positive
Taylor term through degree 84 is enclosed with separate lower-floor and
upper-ceiling integer recurrences on the scale 2^320. The omitted positive
series is bounded by (8/7) times its first omitted term, because each following
term ratio is at most 1/8. Repeated squaring is rounded outward. Negative
arguments use outward-rounded reciprocals of the positive interval. This
includes truncation, arithmetic, range-reduction, and inversion error.

The floor and ceiling operations are integer divisions, not floating-point
approximations. The recurrence and trace formulas use Python exact rationals.
Timing and displayed decimal summaries are the only diagnostic floats.

## Reproduction

From the repository root:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
      python research_20261010/small_seed_order_exclusions/independent_review/audit_orders.py

The script pins one CPU and caps address space at 1 GiB; it imports no BLAS
library. It writes only this review directory. `results.json` contains every
independent interval witness plus the algebra and symmetry ledger;
`INPUT_SHA256.json` seals dependencies; `ACCEPTANCE.json` seals the verdict;
`MANIFEST_SHA256.json` seals the completed review package.
