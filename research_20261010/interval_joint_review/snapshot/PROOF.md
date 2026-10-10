# Continuous ground-only completion through g=.08 using a joint trace constraint

Updated 2026-10-10 15:20 America/New_York (EDT, UTC−4) / 19:20 UTC.
Status: exact candidate; independent joint-lemma and interval reviews required.

## Result

For the ordinary periodic spin-1/2 square bilayer with unit rung coupling,
straight intralayer coupling g, no crossed bonds, and positive-direction
periodic multiplicities, two new closed intervals are certified:

| Closed interval | Initial beta | All integer L≥2 gap lower |
| --- | --- | --- |
| [39/500,79/1000] | 103/10 | 20733752457/1000000000000 |
| [79/1000,2/25] | 207/20 | 4107651847/500000000000 |

Thus [.078,.08] has the uniform lower bound .008215303694. Together with the
unchanged sealed ordinary_interval and interval_extension certificates, the
33-piece union covers all 0≤g≤2/25=.08 and gives a unique finite-volume ground
state and

    gap(H_L(g)) ≥ 486442811/250000000000 = .001945771244

for every integer L≥2. There is no sampling-based interpolation in g or L.
This is a sufficient certificate, not a physical critical coupling.

## Physical inputs are unchanged from the sealed .078 route

Every physical-input construction is exactly the one proved and audited in
`../interval_extension/PROOF.md` and `../interval_extension_review/REVIEW.md`:
fixed auxiliary Temple vectors on 4×4 and 8×4 rungs, a fixed base vector on
8×8 rungs, complete quadratic variance polynomials, the parity-refined
quadratic reference, and a uniform implicit filter at fixed t. The two new
intervals use the .08 auxiliary vectors and newly proposed integer largest
base vectors, whose exact moments are reconstructed from the same audited
matrix polynomials. No production physical vector or new moment is generated.

In particular, for largest shifted Rayleigh rho(g), full residual variance
v(g), and compression bound Rmax at the interval upper endpoint, set

    Cmax=Rmax−min(rho(a),rho(b)),
    vmin=min_[a,b] v(g), t=1/Cmax,
    d=vmin Cmax/(Cmax²+vmin).

The normalized implicit filtered trial has energy ≤rho(g)−d throughout the
interval because v/(1+t²v) is increasing and C(g)≤Cmax. The proof and tests
retain the normalization denominator in this joint fraction. No filtered
residual estimate is claimed. The fixed base has q≤4; the filtered family has
q≤6 and belongs to the original space plus at most one direction, Vψ.

There is still one retained ground level per denominator and one numerator
trial contribution. No odd/triplet trial band is read or counted. Original
search dimensions remain 11/29/29, and the used augmented dimensions are
11/29/≤30. Full Hilbert dimensions remain 4^16/4^32/4^64, with 128 physical
spins on the largest patch. The existing largest full second moment is needed;
H³/H⁴, new geometry contractions, and full diagonalization are not.

The affine correlated energies, uniform Temple widths, complete finite
bosonic tails, directed exponential evaluations, and initial txy triple
(a,b,c) are unchanged. All source polynomials are again checked against the
21 original saved moment files. The initial canonical triple is the reviewed
transport

    A=a sqrt(b), B=a² b sqrt(c), C=a⁴ b² c

at the common post-cycle base (8,8,2beta). The new scalar information below is
what closes [.078,.08]; no additional physical state information is needed.

## New scalar dependency: retain the complete trace-product lower bound

The exact new lemma and rational helpers are frozen in
`../low_band/joint_trace_bootstrap/`, manifest `FROZEN_MANIFEST_1918.json`, SHA-256
905a55c3419a08082c05f8fe011116e2655035c23cb9040e4e92ad856ce4e9bc.
This producer package keeps the new lemma's independent-review requirement
explicit. Finite diagnostic tests do not replace its analytic proof.

If a ladder doubles x,y,time once, its actual consecutive purities p1,p2,p3
satisfy the telescoping identity

    p1⁴ p2² p3 = Z(final)/Z(initial)^8.

All orderings have the same endpoints. At a common base, the actual canonical
product A⁴B²C therefore equals the actual txy product a⁴b²c. Retain the separate
lower bound K=a_l⁴ b_l² c_l from the txy lower endpoints; do not replace it by
the generally smaller product of the separately transported lower endpoints.
Every spatial base here is even, so the reviewed reflected-transfer theorem
gives actual purities in (0,1]. Dropping such factors then yields

    B²C≥K, A²B≥sqrt(K), C≥K.

Let F(z)=1−(1−z)²/(2z²). The new canonical update from lower endpoints is

    D_l=F(max(A_l⁴ B_l² C_l,K)),
    E_l=F(max(B_l⁴ C_l²,K²) D_l),
    F_l=F(max(C_l,K)^4 D_l² E_l),

with downward rounding and positive-output checks. Independently propagate
the txy triple through the usual three updates in its own axis order. At the
new doubled base, transport that new txy triple to canonical order and take
componentwise maxima with the canonical update. Both routes bound exactly
the same canonical labels at exactly the same base, so this maximum is valid.
The next saved K is the downward-rounded maximum of the complete canonical
and txy product lower bounds. If one route fails positivity, only the surviving
route is retained. A nonpositive output is never clipped to a usable value.

The records preserve every txy triple, canonical triple, K, and all canonical
update arguments at each level. Every full step doubles both spatial lengths
and beta. Once the canonical common defect is ≤1/500, the unchanged reviewed
`three_purity_certificate.replay` supplies its analytic asymptotic result.
The coupled iteration itself is never used to invent a new asymptotic theorem.

## Joint-aware finite-size windows

All earlier integer-size windows require a valid bridge before that asymptotic
onset. For lower endpoints s,t and a separate actual-product bound S²T≥P, use

    p=max(s²t,P), w=(1+sqrt(2p−1))/2,
    r=(1−w)/w, d=t/(1+r²),
    I(s,t;P)=(1−r) min(s sqrt(d),d).

The formula requires p>1/2; the spatial step also requires B_l>1/2.
A failed condition returns no positive window bound.

This is the existing dominant-weight argument with its product information
sharpened; it does not replace s,t by inconsistent inferred values. All roots
and outputs are rounded in the directions specified by the frozen helper.
For canonical lower A_l,B_l,C_l and K, use

    sx=max(A_l² sqrt(2B_l−1),sqrt(K) sqrt(2B_l−1)/B_l),
    ty=I(B_l,C_l;K),
    thermal_window_lower=I(sx,ty;0).

The additional spatial expression follows from A²B≥sqrt(K) and monotonicity
of sqrt(2B−1)/B for 1/2≤B≤1. The remaining signed-transfer hypotheses are
unchanged, and every base is an even square. The producer independently checks
that every resulting window gap is positive.

There are 11 saved coupled levels/windows and 12 short-size rows across these
two intervals. The maximum asymptotic onset is L=256. Every integer size
2≤L<256 is accounted for by the relevant short-size bound or closed finite
window. The final bound on each coupling interval is the minimum of all needed
finite windows, its analytic asymptotic result, and its short-size bound.

## Reproduction, inputs, and the preserved weaker route

Run `bash research_20261010/interval_joint_extension/REPRODUCE.sh` from the
repository root. It verifies hashes, reconstructs source polynomials, tests
the interval filter and joint arithmetic, and replays both saved certificates
without eigensolver calls. It also verifies both earlier producer freezes
byte for byte and checks the three adjoining coverage ledgers before asserting
the 33-piece union. The proposal scan took about 1.4 seconds at roughly 50 MiB
RSS; code pins one CPU and numeric thread counts one, with a 1 GiB address-space
cap. No remote action is performed.

`../interval_extension/` remains unchanged. Its independently accepted
0≤g≤.078 result uses the older scalar transport without this new joint lemma,
and already needs no odd-band trial inputs. The present .08 variant has the
same physical input contract and dimensions, but additionally depends on the
joint scalar lemma and joint-aware finite-window theorem. Neither package
inherits the older 0≤g≤.07 route's strict largest-first-moment-only property.
