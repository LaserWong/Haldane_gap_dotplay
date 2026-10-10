# All-six-order small-seed obstruction

Updated: 2026-10-10 14:26 America/New_York (EDT, UTC−4) / 18:26 UTC.

## Statement and scope

The model is the ordinary spin-1/2 square bilayer with unit antiferromagnetic
rung exchange and equal straight in-layer exchange g=1/25 or g=1/20 in both
spatial directions. There are no crossed exchanges. Periodic edges are the
positive-direction multiset, including both parallel bonds when a side is two.

For the seed family 2×2, 4×2, 4×4, the correlated lower-bound recurrence below
has a nonpositive output for every finite real β≥0, for each order xyt, xty,
and txy. Spatial coordinate exchange proves the identical statement for yxt,
ytx, and tyx, using the rotated intermediate seed 2×4 where appropriate.
These statements concern even exact physical partition functions, rather than
only the current lower trace enclosures or a finite temperature scan.

The xty and txy orders fail within their first three updates. Thus neither can
reach a positive first-cycle triple to which the previously reviewed adjacent
swap transport could be applied. The xyt order fails by the fourth update at
g=1/25 and by the second update at g=1/20. Its swapped yxt partner has the same
failure index. The first-cycle-to-canonical recipe therefore fails for all six
orders as well.

This is a method obstruction for these fixed starting seeds and specified
updates. It is not physical gaplessness, a critical coupling, or an obstruction
to larger seeds, additional trace injections, improved inequalities, arbitrary
adaptive changes of order, or other proof methods. In particular, a nonpositive
lower bound on a physical purity does not mean that purity is nonpositive.

## 1. Physical inputs and normalization

Write Z4(β), Z8(β), and Z16(β) for unnormalized physical partition functions
on the three patches, respectively. All six physical complete-band inputs and
their full-space omitted tails were independently reconstructed in
`../small_seed_exclusion_review`. Its accepted `physical_results.json` and the
six exact source hashes are reused; no new trial vector or physical spectral
claim is introduced here. The current script verifies the acceptance hash and
every physical-audit input hash before the calculation and verifies them again
at completion.

For a patch with N rungs, H′=H+3N/4. Let s be the retained ground upper endpoint
for H′ and E=−3N/4+s. Then Z(β)=exp(−βE)T(β). The certified trace lower bound is

    L(β) = sum over retained states m_i exp[−β(u_i−s)],

and the upper bound is

    U(β) = sum over retained states m_i exp[−β(l_i−s)]
           + sum over omitted bins M_q exp[−β(a_q−s)].

The physical audit establishes every retained endpoint and every omitted-bin
multiplicity. There are 1+3N retained states, and the total upper multiplicity
is exactly 4^N. The code separately verifies both counts and that the omitted
tail begins at ordered index 2+3N. All retained upper gaps u_i−s are
nonnegative. Negative lower gaps are allowed in U and handled by their sign.

## 2. Correlated first cycle at the correct basepoints

Let v=(2,2,β) and D_i double coordinate i. For any permutation (i,j,k), define
v1=D_i v, v2=D_jD_i v, v3=D_kD_jD_i v=(4,4,2β). Set

    q1 = Z(v1)/Z(v)^2,
    q2 = Z(v2)/Z(v1)^2,
    q3 = Z(v3)/Z(v2)^2.

The reviewed even-length spatial-transfer and Gibbs identities make all q_i
purities in (0,1]. Exact cancellation gives

    J1 = q1^4 q2^2 q3 = Z(v3)/Z(v)^8,
    J2 = q2^4 q3^2    = Z(v3)^2/Z(v1)^8,
    C0 = q3          = Z(v3)/Z(v2)^2.

The scalar lower-bound recipe is

    G(z) = 1−(1−z)^2/(2z^2),
    a = G(J1),
    b = G(J2 a),
    c = G(C0^4 a^2 b).

An output is used only if every prior output is positive. When positive,
(a,b,c) bounds the same ordered staircase (i,j,k) at v3; it is not a
relabeled canonical staircase. Subsequent fixed-order cyclic outputs are
G(a^4 b^2 c), followed by a queue shift.

For the representative orders the inputs are exactly:

- xyt: J1=Z16(2β)/Z4(β)^8;
  J2=Z16(2β)^2/Z8(β)^8; C0=Z16(2β)/Z16(β)^2.
- xty: the same J1 and J2;
  C0=Z16(2β)/Z8(2β)^2.
- txy: the same J1;
  J2=Z16(2β)^2/Z4(2β)^8; C0=Z16(2β)/Z8(2β)^2.

The corresponding physical energy factors are

    J1:             exp[β(8E4−2E16)],
    J2 spatial-first: exp[β(8E8−4E16)],
    J2 time-first:  exp[β(16E4−4E16)],
    C0 time-last:   1,
    C0 space-last:  exp[β(4E8−2E16)].

The temperature-doubled denominators in the last two alternatives are crucial.
No physical spatial coordinate is exchanged with temperature, and energy
offsets are canceled explicitly rather than assumed extensive.

## 3. Why a nonpositive upper output is an obstruction

On 0<z≤1, G′(z)=(1−z)/z^3≥0 and G(z)≤1. Starting from upper bounds
(J1+,J2+,C0+) in (0,1], propagate the same formulas with upward rational
rounding. If the exact-input lower-bound recipe has stayed positive, its next
argument is no larger than the corresponding upper argument. All intervening
products are monotone because their factors are nonnegative. Its next output
is therefore no larger than the propagated upper output.

If the latter is negative, either an earlier exact recipe output was already
nonpositive, or this one is. This proves failure of the lower-bound recipe.
The algorithm stops immediately on failure and never substitutes a negative
entry into later products. Exact arithmetic checks 0<argument≤1 at every
visited positive step. Clipping a physical input upper bound to one is valid
because the q-products above are at most one.

## 4. Hot interval: 0≤β≤4

Use the txy path merely as a factorization of the common J1:

    J1 = T4(β)^4 P_x(2,2,2β)^2 P_y(4,2,2β) ≤ T4(β)^4,
    T4(β) = Z4(2β)/Z4(β)^2.

Here both spatial factors are genuine even-base purities. For a fixed physical
Hamiltonian, d log T4/dβ=2(〈H〉_β−〈H〉_2β)≥0, since
d〈H〉_β/dβ=−Var_β(H)≤0. Therefore J1≤T4(4)^4 throughout the hot interval.
No monotonicity of spatial purity with inverse temperature is assumed.

Exact trace bounds give T4(4)≤U4(8)/L4(4)^2. For both couplings, the rational
upper enclosure of G([U4(8)/L4(4)^2]^4) is strictly negative. Consequently all
orders fail at their first update throughout 0≤β≤4. This includes β=0.

## 5. Closed middle boxes: 4≤β≤20

The script evaluates all 320 closed boxes

    [4+k/20, 4+(k+1)/20],  k=0,…,319.

They cover the entire interval, share endpoints, and leave no gaps. On each
box [l,h], an upper term exp(−βe) uses β=l when e≥0 and β=h when e<0.
A lower term uses the opposite endpoint. An energy factor exp(βd) uses β=h
when d≥0 and β=l when d<0. These choices give simultaneous uniform enclosures
of every numerator and denominator at the same actual β in the box.

Every numerator is bounded above and every denominator below, using the exact
factors in Section 2. The common numerator is U16([2l,2h]), with its square for
J2. Denominators are L4([l,h])^8, L8([l,h])^8, L4([2l,2h])^8,
L16([l,h])^2, or L8([2l,2h])^2 as appropriate. All three order-specific upper
triples are propagated separately. Each box has a strictly negative upper
output within three steps for xty/txy and within four steps for xyt.

Every individual interval, input triple, argument, and output is saved as an
exact rational in `results.json`. Floating summaries are not proof steps.
The rational exponential engine uses 256-bit directed dyadic rounding and a
70-term positive Taylor expansion after range reduction; its truncation and
rounding errors are included in both endpoints. It is the already separately
reviewed `../low_band_review/fast_exp.py`, whose hash is recorded.

## 6. Unbounded cold ray: β≥20

Let E16− be the certified physical ground lower endpoint and let Urel be the
4×4 trace upper sum rebased at it. Every retained and tail lower gap relative
to E16− is nonnegative, checked exactly. Thus

    Z16(2β) ≤ exp(−2βE16−) Urel(40)   for all β≥20.

Keeping only the actual ground term in each denominator and using its upper
energy endpoint gives

    J1 ≤ exp(−20 d1) Urel(40),
    J2 spatial-first ≤ exp(−20 dx) Urel(40)^2,
    J2 time-first ≤ exp(−20 dt) Urel(40)^2,

where

    d1 = 2E16−−8E4+ > 0,
    dx = 4E16−−8E8+ > 0,
    dt = 4E16−−16E4+ = 2d1 > 0.

The exact positivity of all three slopes is verified. Together with the
universal C0≤1, these uniform input upper bounds fail by update two at g=1/25
and update one at g=1/20, for all three representative orders. This covers
the entire unbounded ray, not an extrapolation from finitely many points.

## 7. Exact spatial exchange and six orders

For arbitrary rectangle dimensions nx,ny, relabel every physical spin site
(x,y,layer) as (y,x,layer). This is a bijection and hence induces a unitary
permutation of the full tensor-product Hilbert basis. Each rung bond maps to a
rung bond; each positive x bond maps to a positive y bond, and vice versa.
All bond multiplicities are preserved, including the two-edge periodic sides.
Because the two in-layer couplings are equal, this unitary conjugates H(nx,ny)
to H(ny,nx), with no change in β. Therefore

    Z(nx,ny;β) = Z(ny,nx;β).

Exchange x↔y along the entire ordered path and all its basepoints, not just
the labels on three measured values. Every q, J1, J2, C0, and recurrence output
is then identical. This gives exactly the pairs xyt↔yxt, xty↔ytx, and txy↔tyx.
The executable also verifies the edge-multiset bijection for every seed shape;
the general bijection above supplies the analytic proof beyond these checks.

## Reproduction and limits

From the repository root:

    PYTHONDONTWRITEBYTECODE=1 python research_20261010/small_seed_order_exclusions/certify_orders.py

This writes only this directory, changes no accepted input, and makes no remote
write. It pins one CPU, forces all BLAS backends to one thread, and limits the
process address space to 1 GiB. It performs rational scalar arithmetic only:
no physical vector construction, new physical moment calculation, or full
diagonalization. The prior accepted physical reconstruction remains an explicit
dependency, rather than being falsely described as repeated here. Independent
review of this new scalar extension is recorded separately.
