# Small seed, information-preserving mixed-cube scalar test

Updated 10 October 2026, 17:04 EDT / 21:04 UTC.

## Status and precise conclusion

The bounded scan and directed rational selected-point replay find no rescue at
g=1/25 or g=1/20. In addition, the new position-wise upper-envelope argument
below, checked on all previously certified closed temperature boxes and hot/cold
rays, gives a **candidate all-beta exclusion of the explicitly defined mixed-cube
algorithm**. It awaits a separate analytic and implementation review.

This is a new argument. The older exclusion of six isolated fixed cyclic orders
is not applied to the new recursion. Only its independently accepted physical
quotient upper enclosures, temperature coverage, and coordinate-exchange result
are reused as input data.

The model is the ordinary spin-1/2 bilayer, rung coupling 1, equal straight
in-layer couplings g, no crossed exchanges, periodic positive-direction edge
multiplicities. The physical supports remain 2x2, 4x2, and 4x4 rungs (or their
x/y reflections). The largest Hilbert space is 4^16=2^32, with 49 retained low
states; the saved largest ground search dimension is 11. There is no new physical
vector, support, moment, or full diagonalization.

## 1. Cube notation and permitted information

At an even spatial base v=(n,m,beta), let D_i double axis i in {x,y,t}. For a
subset S of axes, D_S applies those doublings once. Write

    p_i(S) = Z(D_(S union {i})v) / Z(D_S v)^2, i not in S.
    Q_ij(S) = Z(D_(S union {i,j})v) / Z(D_S v)^4.
    K = Z(D_{x,y,t}v) / Z(v)^8.

There are 12 edges and six squares. Exact cancellation gives

    Q_ij(S) = p_i(S)^2 p_j(S union {i})
            = p_j(S)^2 p_i(S union {j}).
    K = p_i(empty)^4 Q_jk({i})
      = Q_ij(empty)^2 p_k({i,j}).

All actual edges belong to (0,1] under the inherited reflected even-base transfer
hypotheses. Only lower bounds are stored. Initial edge, square, and full-product
bounds are independently formed from the saved physical trace bounds, with all
energy shifts and temperature labels restored. In the exact-input comparison
algorithm they are the exact physical quotients.

The following lower-information operations may be applied arbitrarily often,
in any order, at this same cube base:

1. Maximize compatible edge bounds and compatible square/full-product bounds.
2. Form a square lower bound from either oriented pair p^2 q.
3. From a square lower bound Q, infer first-edge sqrt(Q) and second-edge Q,
   separately in either orientation. This is the adjacent-swap transport.
4. Form K from either displayed factorization.
5. From K infer Q_ij(empty)>=sqrt(K) and Q_jk({i})>=K; apply step 3 as desired.

These operations preserve independently supplied full and partial products;
they never replace a stronger product constraint by the product of weakened
individual transported bounds. They include the accepted joint-aware canonical
update and all six order transports. Direct consequences K^(1/4),sqrt(K),K for
the first, second, third edges follow from these rules. Simultaneous lower bounds
need not be attained by one endpoint tuple.

At the initial cube, the exact physical edge/square/product data are unchanged
by these operations: every product identity is exact and every factor-dropping
deduction only lowers an actual edge. Thus initial closure cannot exceed the
exact physical starting information.

## 2. Purification and correct basepoints

Put G(z)=1-(1-z)^2/(2z^2). For order (i,j,k), the usual rotating ladder gives
the following three new edges at the fully doubled base v'=D_{x,y,t}v:

    d_i at p_i'(empty) >= G(K),
    e_ij at p_j'({i}) >= G(Q_jk({i})^2 d_i),
    f_ijk at p_k'({i,j}) >= G(p_k({i,j})^4 d_i^2 e_ij).

All six routes are attempted. Every positive partial output is retained even
when that order's later output is nonpositive. At v', merge all partial outputs
and apply every allowed same-base closure operation. After another complete
cycle, the base is D_{x,y,t}v'=(4n,4m,4beta). Old K is never reused at v'.

For canonical lower components a,b,c and independently retained K, the second
argument above includes max(b^4 c^2,K^2)d, and the third includes
max(c,K)^4 d^2 e. Hence this algorithm genuinely includes the accepted new
joint-ratio recursion. It is stronger than propagating only completed raw
ladders, because unfinished orders also contribute their valid first/second
edges and their transported consequences.

Repeated complete cycles, conversion to canonical order at any completed cube,
and mixing those same-base bounds are covered. Arbitrary nonsynchronous changes
at other, noncommon bases, new trace injections (even on the same physical
support at additional temperatures), different inequalities, and stronger
optimization over the full constraints are not asserted to be covered.

## 3. A new invariant upper envelope

This section bounds the outputs of a lower-bound algorithm, not the physical
purities. Suppose all stored first-position edge lower endpoints are at most D,
all second-position endpoints at most E, all third-position endpoints at most F,
where 0<=D,E,F<=1. Also cap root squares by R=D^2 E, suffix squares by S=E^2 F,
and the full joint lower endpoint by T=D^4 E^2 F.

Every permitted closure operation preserves these caps:

- Edge products give root squares at most D^2 E and suffix squares at most E^2 F.
- Root-square deductions give first edges <=D sqrt(E)<=D and second edges
  <=D^2 E<=E.
- Suffix-square deductions give second edges <=E sqrt(F)<=E and third edges
  <=E^2 F<=F.
- Either full-product factorization gives K<=D^4 E^2 F.
- K-to-root-square gives sqrt(K)<=D^2 E sqrt(F)<=R.
- K-to-suffix-square gives K<=D^4 E^2 F<=S.
- Maxima of compatible bounds preserve each cap.

This invariant proves the result for arbitrarily many closure steps, independent
of the finite 16-sweep diagnostic implementation and independent of the order
of scalar deductions. No convex optimization or tuple-attainment assumption is
being made.

For one beta interval let j bound all initial common K, q bound all initial
Q_jk({i})^2, and c bound every initial last-edge p_k({i,j}). All are in (0,1].
Let

    D=G(j), E=G(qD), F=G(c^4 D^2 E).

G is increasing on (0,1], with derivative (1-z)/z^3. Thus these are uniform
upper caps for every positive output of all six first-cycle routes. Taking q
and c separately maximized over different orders deliberately enlarges the
algorithm's possible output and is safe for exclusion. Upward rounding remains
safe. Stop at the first nonpositive cap, without substituting it into a later
nonlinear product.

If D<=0, no first output is positive. If E<=0, all second/third edges remain
unavailable, and closure cannot produce them from first edges alone. If F<=0,
all third edges remain unavailable and no positive full joint can be formed.
Otherwise the fully doubled cube satisfies K_new<=D^4 E^2 F under every closure.
If G(D^4 E^2 F)<0, no subsequent first purification output can be positive,
regardless of which order is chosen or how often information was transported.
This obstructs repeated-cycle bootstrap. It also prevents a small-defect onset:
three canonical bounds >=499/500 would already force a joint lower endpoint
> (499/500)^7, whereas the last case has K_new<sqrt(2)-1.

## 4. Temperature coverage and exact records

The previously independently accepted data provide:

- On [0,4], common K <= T_2x2(4)^4, from monotonicity of physical Gibbs purity.
- On each of 320 closed boxes [4+k/20,4+(k+1)/20], k=0,...,319, upper bounds for
  common J1=K, order-specific J2=Q_jk({i})^2, and last-edge C0=p_k({i,j}).
- On [20,infinity), uniform quotient bounds from positive physical energy
  curvature slopes and nonnegative rebased relative energies, with C0<=1.
- Exact x/y reflection gives all six orders from xyt, xty, txy.

The new script takes orderwise maxima, evaluates the new envelope, and saves
every argument and 320-bit upward-rounded output. It does not read or rely on
the old failure stages to establish the new result. Dependency hashes are
checked against the independent prior acceptance manifest.

Middle-box failure counts for the enlarged envelope are:

| Coupling | D stage | E stage | F stage | next-cycle first stage |
|---|---:|---:|---:|---:|
| 1/25 | 18 | 139 | 81 | 82 |
| 1/20 | 149 | 171 | 0 | 0 |

The hot range fails at D. The cold range also fails before a complete new cube.
Every saved witness is strictly negative; the closest middle witnesses are
approximately -0.000910781697745729 and -0.005434655727955548 respectively.

## 5. Bounded diagnostic and minimum-seed wording

The separate floating diagnostic scans beta=1,...,60 with spacing 1/40 (2,361
points per coupling), all six orders, up to 16 cube cycles and 16 closure sweeps
per cube. Eight selected points are reconstructed with directed rational trace
enclosures and 256-bit downward rounding. No candidate reaches a positive
asymptotic certificate; therefore no new all-integer-L gap or finite-window
bridge is claimed.

At g=1/25 the largest scanned first doubled-base joint lower bound occurs at
beta=337/40. Its directed rational replay gives approximately 0.324447952058220,
with next G output approximately -1.167691924568251. At g=1/20 no positive full
first-cycle joint is obtained anywhere on the grid.

Even after separate acceptance of the new envelope, a statement that this is
the mathematically minimum seed among all methods would be unjustified. The
result excludes only the defined information-preserving mixed-cube scalar
method at g=.04/.05. Other inequalities, additional trace injections, different
geometries, or more general adaptive recursions remain open. The original
all-beta six-fixed-order result keeps its original narrower scope.

## 6. Reproduction and review boundary

Run scan_joint_small.py for the bounded diagnostic and certify_envelope.py for
the new all-beta candidate. They write this directory only. Each uses one pinned
CPU and a 1 GiB address-space cap. No frozen/root file or remote repository is
modified. Selected-point rational arithmetic is separate from floating proposal
ranking; no floating proposal is treated as a certificate.

Physical complete-band/full-tail correctness is inherited from the explicitly
accepted small_seed_exclusion_review. This package does not claim a fresh
physical reconstruction or a separate reviewer acceptance of its new lemma.
