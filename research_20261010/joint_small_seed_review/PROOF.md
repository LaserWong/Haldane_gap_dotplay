# Independent review of the mixed-cube small-seed obstruction

Updated 2026-10-10 17:14 America/New_York (EDT, UTC−4) / 21:14 UTC.

## Verdict

**PASS for the precisely defined synchronous mixed-cube lower-bound algorithm.**
The new invariant is valid. Its all-temperature numerical hypotheses pass an
independent exact replay of all 644 records. This conclusion does **not** follow
from the old six-fixed-order exclusion, and that exclusion is not used here.
Only its sealed, independently accepted physical quotient upper enclosures,
temperature coverage, and spatial exchange proof are inherited.

For the ordinary spin-1/2 square bilayer, rung coupling 1, equal straight
in-layer couplings g=1/25 or 1/20, no crossed exchange, and periodic
positive-direction bond multiplicities, the 2×2 / 4×2 / 4×4-rung seed (including
its x/y reflection) cannot start this mixed-cube bootstrap at any finite
physical inverse temperature β≥0, even if its initial partition functions are
known exactly. The conclusion concerns the scalar **lower-bound algorithm**;
it is not an upper bound on the actual later physical purities.

There is one harmless wording error in the producer proof: three endpoints
≥499/500 imply a product **≥**(499/500)^7, not necessarily strictly greater.
The latter number is itself strictly larger than sqrt(2)−1, so replacing the
first strict sign by a weak sign leaves the conclusion unchanged. This review
also explicitly checks the original cube cannot already meet that onset
threshold; the producer paragraph explicitly discusses only the new cube.
No producer file has been edited.

## 1. Formal state and the exact scope of the algorithm

Let I={x,y,t}, with t denoting inverse-temperature doubling, not a spatial
coordinate. At a cube base v=(n,m,β), both n and m are even. For S⊆I, D_S doubles
those coordinates once, and

    p_i(S) = Z(D_(S∪{i})v) / Z(D_S v)^2,       i∉S,
    Q_ij(S) = Z(D_(S∪{i,j})v) / Z(D_S v)^4,   i,j∉S,
    K = Z(D_I v) / Z(v)^8.

A state consists of 12 edge lower endpoints, six square lower endpoints, and
one full-product lower endpoint. The edge's positional depth is |S|: first,
second, or third. There are three root squares with S=∅ and three suffix
squares with |S|=1. The full-product label is common to all six permutations.
An unavailable positive lower endpoint is represented by zero. Bounds may be
simultaneously true without their endpoints being jointly attained.

Initial endpoints are independently supplied by valid physical trace bounds,
or by the exact physical quotients in the stronger comparison algorithm. At a
fixed cube base, the complete allowed closure grammar is:

1. Take a maximum only for the same edge, square, or full-product label.
2. For either orientation of a square, form q≥a²b from its two edge bounds.
3. From that square bound q, infer a≥sqrt(q) and b≥q in **either** orientation.
4. For each permutation (i,j,k), form a full-product bound from
   p_i(∅)^4 Q_jk({i}) or Q_ij(∅)^2 p_k({i,j}).
5. From a full-product bound k, infer every root-square bound sqrt(k) and
   every suffix-square bound k. Rules 1–4 can then be repeated.

Only lower endpoints are propagated. Existing independently supplied products
are retained by maxima, rather than overwritten by products of weaker
component endpoints. The grammar does not include solving a joint constrained
optimization problem, importing a new trace, dividing by an additional bound,
or moving a state to a different base without the prescribed purification.

At a full-cycle transition, the new base is v′=D_I v. Start a fresh state there.
For all six orders (i,j,k), attempt the following outputs successively:

    d_i = G(K),
    e_ij = G(Q_jk({i})² d_i),
    f_ijk = G(p_k({i,j})⁴ d_i² e_ij),
    G(z) = (z²+2z−1)/(2z²).

Only positive outputs enter the new state, but a positive d or e is kept when
a later output of the same route fails. Their precise labels in the new cube
are p_i′(∅), p_j′({i}), p_k′({i,j}). Merge all such outputs and apply the closure
grammar arbitrarily often. Repeat only from that common new base. The old K
is not retained under the new full-product label.

The producer diagnostic implements this grammar with 16 closure sweeps and up
to 16 cycles. Our exclusion allows arbitrarily many sweeps and cycles and is
therefore independent of those diagnostic limits. No floating scan result is
used in the acceptance calculation.

## 2. Soundness, orientations, and basepoint bookkeeping

Every relevant actual edge lies in (0,1] under the inherited reflected
self-adjoint spatial-transfer and Gibbs hypotheses. For a spatial edge, it is
the normalized spectrum of an **even power** of a self-adjoint transfer that
provides nonnegative probability weights. The transfer itself need not be
positive semidefinite. Every spatial length in this cube construction starts
even and stays even under doubling. A thermal edge is a Gibbs purity of the
fixed finite-dimensional Hamiltonian. No spatial/time unitary exchange is used.

Exact cancellation gives

    Q_ij(S) = p_i(S)² p_j(S∪{i})
            = p_j(S)² p_i(S∪{j}),
    K = p_i(∅)^4 Q_jk({i})
      = Q_ij(∅)² p_k({i,j}).

The swapped pair has the same prefix and terminal vertex. Thus its first edge
stays at depth |S| and its second edge stays at depth |S|+1; exchanging axes
does not exchange positional caps. Dropping factors bounded above by one
justifies the square roots and unsquared deductions in the grammar. It also
justifies K-to-square deductions. These are lower inequalities, not assertions
that an endpoint tuple realizes the underlying equalities.

At the initial cube, storing exact physical values already fixes every label
at its largest physically possible endpoint. All closure rules preserve valid
lower bounds, so none can increase a label past that exact value. Less precise
initial lower bounds likewise cannot exceed it after closure. This is why
uniform physical upper enclosures on the initial K, suffix squares, and last
edges are valid inputs to the new obstruction.

For completeness, the first purification follows by dropping the other-axis
factors to obtain P_i(D_j D_k v)≥K, then squaring the i-spectrum. This produces
P_i(D_I v)≥G(K). Rotate the ladder to order (j,k,i) at D_i v. Its queue is the
two old suffix edges followed by the new d_i, so its product is
Q_jk({i})² d_i. Rotating once more to (k,i,j) produces
p_k({i,j})⁴ d_i² e_ij. The three output basepoints are, respectively,
v′, D_i v′, and D_j D_i v′. After the three rotations, the original order is
restored at v′. These statements are verified by an independent integer
coordinate ledger for all 18 updates, plus all 12 oriented square identities
and all 12 full-product factorizations.

The closure includes the accepted joint-aware canonical update: the stored
suffix square is at least max(b²c,K), and the last edge is at least max(c,K).
Consequently its second and third arguments include
max(b⁴c²,K²)d and max(c,K)⁴d²e. Conversely, no previously retained joint is
silently replaced by a weak component product. The audit's stress tests start
with separate products stronger than the products of its component endpoints.

Spatial reflection maps (x,y,layer) to (y,x,layer). It preserves rung exchanges
and the complete positive-direction in-layer multiset, including parallel
periodic bonds when a side is two. Equal x/y couplings therefore give equal
partition functions on reflected paths at the same physical β. This supplies
exactly xyt↔yxt, xty↔ytx, and txy↔tyx. Full-spin multiset checks for 2×2, 4×2,
2×4, and 4×4 supplement this analytic bijection. An axis relabeling without
its full path and basepoints would not suffice.

## 3. Universal invariant for the closure

Assume 0≤D,E,F≤1. Impose the following caps on **algorithmic endpoints**:

    depth-zero edges ≤ D,
    depth-one edges  ≤ E,
    depth-two edges  ≤ F,
    root squares    ≤ R = D²E,
    suffix squares  ≤ S = E²F,
    full product    ≤ T = D⁴E²F.

Each generating operation preserves these caps:

- Products of oriented edge pairs are at most R or S according to depth.
- A root-square bound produces a first edge ≤sqrt(R)=D sqrt(E)≤D and a
  second edge ≤R=D²E≤E.
- A suffix-square bound produces a second edge ≤sqrt(S)=E sqrt(F)≤E and a
  third edge ≤S=E²F≤F.
- Either full-product factorization is at most D⁴S=R²F=T.
- K-to-root gives sqrt(T)=D²E sqrt(F)≤R.
- K-to-suffix gives T=D⁴E²F≤S.
- Taking maxima of endpoints with the same label preserves its cap.

The executable separately represents these ten operation classes as monomials
in independent D,E,F, allowing exact rational half-exponents. Every output
exponent vector dominates its target cap's vector coordinate by coordinate,
which proves the inequality throughout [0,1]^3. This is an independently
checkable encoding of the displayed analytic proof, not a sample-based claim.

Induction proves invariance after any finite operation sequence. Supremums of
such bounded sequences remain in the same closed cap intervals, so arbitrarily
many closure sweeps do not change the conclusion. No tuple-attainment,
convexity, fixed sweep count, or fixed axis order enters this proof.

### Positive partial routes and missing positions

Negative caps are never substituted into a later product.

- If the first cap is nonpositive, no positive first output exists.
- If the second cap is nonpositive, at most first edges have been seeded.
  A square needs a second edge as well as a first edge; no positive square,
  later edge, or full product can be generated from first edges alone.
- If the third cap is nonpositive, only first and second edges can be seeded.
  Root squares may be formed and transported, but every suffix square needs
  a third edge, and every full-product factorization needs either a third
  edge or a suffix square. Thus no positive third edge or full product can
  arise. The first/second/root cap argument is still closed by itself.

These are support-invariant arguments, not an assumption that failed routes
were thrown away. The executable exhausts all 8 subsets of first-edge seeds
and all 512 subsets of first/second-edge seeds using the full Boolean closure
grammar. Neither can create a missing deeper position or full joint. Boundary
stress tests additionally perform 60,000 arbitrarily ordered rational scalar
updates over 125 D/E/F boundary states, retaining independent product bounds.

## 4. All-temperature physical envelope and exclusion

For a particular uniform β-domain, let j bound the exact initial K, let q
bound every exact initial Q_jk({i})², and let c bound every exact initial last
edge. The physical inputs satisfy 0<j,q,c≤1. On (0,1],

    G′(z) = (1−z)/z³ ≥ 0,        G(z)≤1.

Set, successively and stopping on a nonpositive result,

    D = G(j),
    E = G(qD),
    F = G(c⁴D²E).

These are upper caps for every positive output of the six routes. Separately
maximizing q and c, even when they come from different orders, only enlarges
the cap and is therefore safe for an exclusion. Upward dyadic rounding is also
safe and stays ≤1. The actual computation uses these enlarged rounded caps.

If D,E,F are positive, the fresh state starts inside all the cap intervals:
its independent square/full-product stores initially contain only zero; later
values come exclusively from the grammar. Section 3 gives

    K_new ≤ D⁴E²F.

Every recorded box with three positive caps then has
G(D⁴E²F)<0. Hence no first output at the next common cube can be positive,
regardless of the selected order or any amount of allowed same-base transport.
The other boxes have already failed by the partial-support arguments.

### Physical inputs actually used

Write Z4,Z8,Z16 for the unnormalized physical traces on the three patches.
For the three representative orders, the inherited upper triples bound:

    common j: Z16(2β) / Z4(β)^8;
    xyt q:   Z16(2β)^2 / Z8(β)^8;
    xyt c:   Z16(2β) / Z16(β)^2;
    xty q:   Z16(2β)^2 / Z8(β)^8;
    xty c:   Z16(2β) / Z8(2β)^2;
    txy q:   Z16(2β)^2 / Z4(2β)^8;
    txy c:   Z16(2β) / Z8(2β)^2.

Thus the order-specific denominators retain their doubled temperatures.
For ZN(β)=exp(−β EN) TN(β), the physical energy factors have slopes
8E4−2E16, 8E8−4E16, 16E4−4E16, 0, and 4E8−2E16, respectively.
The inherited physical reconstruction checks EN=−3N/4+sN, all retained level
endpoints, complete-band counting, and the full omitted tail. Its accepted
result hash is
6e78a354da036930520761566f0b255761b8baf6363e8caa6b2c3bb41ba77fa3.
No fresh many-body reconstruction or new exponential evaluation is claimed in
this review; accepted exact scalar upper inputs are reused as sealed data.

The coverage is uniform:

- On [0,4], K≤T4(4)^4. Only Gibbs purity's temperature monotonicity is used.
  No spatial-purity monotonicity is assumed.
- The 320 closed intervals [4+k/20,4+(k+1)/20], k=0,…,319, cover [4,20]
  with matching endpoints. Their quotient inputs are uniform interval
  enclosures, not point samples.
- On [20,∞), the 4×4 upper trace is rebased at its certified ground lower
  endpoint. Nonnegative relative energies give a uniform numerator bound at
  2β≥40; positive exact curvature slopes control all ground-denominator
  factors. The last-edge bound c≤1 completes the cold ray.

At both couplings, all inherited producer quotient endpoints are checked
against the sealed prior independent endpoints, which are no larger. This
checks 5,778 rational middle/cold scalar comparisons, plus the hot quotient
and thermal-purity comparisons. The old fixed-order failure indices, old
recurrence histories, and old no-go assertion are not used.

### Independent arithmetic results

All 640 closed middle boxes plus four hot/cold ray records pass. For each
record, the review recomputes the orderwise maxima, every exact argument,
every 320-bit upward-rounded output, the first negative stage, and its witness.
G is evaluated by integer numerator/denominator arithmetic independently of
the producer's rational-expression implementation. For z=n/d its numerator
is n²+2nd−d² and its denominator is 2n²; a quotient/remainder test implements
the directed ceiling. Every visited argument is checked in (0,1], and no
negative output is reused.

The middle-box failure counts are:

| g | D | E | F | next first |
|---|---:|---:|---:|---:|
| 1/25 | 18 | 139 | 81 | 82 |
| 1/20 | 149 | 171 | 0 | 0 |

The closest negative witnesses are approximately −0.0009107816977457291 and
−0.005434655727955548. Both occur on [273/20,137/10], at stages E and D,
respectively. The hot rays fail at D; the cold rays fail at E for 1/25 and D
for 1/20. All acceptance comparisons use exact rationals, not these decimals.

For 1/25, the largest completed first-cube joint cap over the accepted boxes
is approximately 0.3354651325502786 on [167/20,42/5], below sqrt(2)−1. At 1/20
no box has a positive full first-cube joint. These are enlarged algorithmic
upper caps, not achieved values or bounds on actual physical purities.

### Small-defect onset, including the initial cube

Three canonical endpoints ≥r=499/500 imply their generated joint lower
endpoint ≥r^7. Exact rational arithmetic verifies (r^7)^2+2r^7−1>0, so
r^7>sqrt(2)−1. Such a triple cannot occur in a completed new cube. A partial
cube lacks a required positive edge and cannot satisfy the onset condition.

At the original cube, the maximum inherited all-temperature upper cap on the
actual K is approximately 0.6993506667232421 for 1/25 and 0.58368086599694 for
1/20. Both are strictly below r^7≈0.9860837205593285. Thus the original cube
also cannot bypass purification by already satisfying that onset condition.
This extra explicit check closes a minor exposition gap without altering any
producer input or enlarging the claimed no-go scope.

## 5. Adversarial tests and exclusions from the conclusion

`ADVERSARIAL_TESTS.json` records the structural tests above and deliberately
invalid extensions that the audit rejects:

- Reusing the old K at the new cube produces a positive first G output in a
  saved box whose correctly bounded new K gives a negative output.
- A separately supplied K can be stronger than the product of weak component
  endpoints; it must be retained. The cap proof never assumes endpoint equality.
- For the signed transfer diag(1,−1/16), the even-base purity is below one but
  the odd-base ratio exceeds one. The cap argument is not extended to odd bases.
- Exact Ising transfer values show spatial purity can decrease under cooling.
  Numerical reordering of old values is not licensed by order symmetry.

The accepted obstruction is restricted to the synchronous complete-cube
algorithm in Section 1 with the listed same-base closure grammar. It does not
exclude new trace injections, including additional temperatures on the same
physical supports; asynchronous direction changes at other, noncommon bases;
stronger optimization over all simultaneous constraints; additional
inequalities; other geometries; larger seeds; or other proof methods.
It is not physical gaplessness, a phase boundary, a global minimum-seed theorem,
or a new all-integer-L gap certificate. A successful late cube in some future
method would still require all preceding finite-size bridges.

The largest inherited physical support remains 16 rungs / 32 spins, complete
Hilbert dimension 4^16=2^32. Its retained complete low band has 49 states, and
its saved ground search dimension is 11. No new physical state, support,
moment, MPS bond dimension, or full diagonalization is introduced.

## 6. Reproducibility and integrity

Run from any directory:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
      PYTHONDONTWRITEBYTECODE=1 python audit_envelope.py

The script resolves dependencies relative to its own path and writes only
this review directory. It uses one pinned CPU and a 1 GiB address-space cap;
the acceptance run took about 1.18 seconds and 36 MiB RSS. It imports no project
implementation and never executes producer code. Eighty sealed input files
were checked before and after the audit. The producer package seal, prior
independent scalar acceptance, physical acceptance, physical source seals,
and exact input hashes are all verified.

`results.json` saves every newly recomputed record. `INPUT_SHA256.json` seals
the exact inherited inputs. `ACCEPTANCE.json` seals the verdict and scope.
`MANIFEST_SHA256.json` seals this completed review package. The working tree is
an extracted snapshot without Git metadata; no local commit or GitHub
publication is asserted. No producer, root, or remote file was modified.
