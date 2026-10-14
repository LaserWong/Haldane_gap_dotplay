# Independent joint-ratio and basepoint audit

Updated 10 October 2026, 15:18 America/New_York (EDT) / 19:18 UTC.

## Result and scope

The proposed joint-ratio scalar improvement is analytically valid under the previously audited reflected even-base transfer hypotheses. Its one- and two-dimensional recursion and finite-window formulas are accepted as scalar lemmas. This does not, by itself, certify any new physical coupling. New partition-function inputs, directed arithmetic, and every intervening finite window must each be audited for a model-specific result.

The workspace is an extracted shared snapshot without Git metadata. This review neither edits frozen generating packages nor claims a commit or remote publication.

## 1. Exact common endpoints and order independence

Let v record all spatial lengths and the physical inverse temperature beta.
D_i doubles exactly coordinate i. For an ordered ladder with k axes, put
v_0=v, v_j=D_(i_j)v_(j-1) and p_j=Z(v_j)/Z(v_(j-1))^2. Exact cancellation gives

    product_(j=1)^k p_j^[2^(k-j)] = Z(v_k)/Z(v_0)^[2^k].

The exponents and all temperature labels matter. Doublings commute, so the right side is common to all direction orders with the same initial base.

For a chain, with canonical S=P_x(v), T=P_t(D_x v), and time-first
 a=P_t(v), b=P_x(D_t v), the exact identity is

    S^2 T = a^2 b = Z(2n,2 beta)/Z(n,beta)^4.

For two spatial directions, with canonical A=P_x(v), B=P_y(D_x v),
C=P_t(D_y D_x v), and time-first a=P_t(v), b=P_x(D_t v),
c=P_y(D_x D_t v), it is

    A^4 B^2 C = a^4 b^2 c = Z(2n,2m,2 beta)/Z(n,m,beta)^8.

A time-first cycle starting at (n,beta) ends with a time-first ladder based at (2n,2 beta), not at (2n,beta) or (n,2 beta). In two dimensions it ends at (2n,2m,2 beta). After r full cycles every spatial base and beta is multiplied by 2^r. Only then does order transport change the edge labels. It leaves that common base unchanged.

`verify_lemma.py` independently verifies full product identities, adjacent square identities and rotating-ladder basepoints by integer exponents of formal partition functions for every permutation of two, three and four axes and four successive cycles. These exact algebraic checks supplement, rather than replace, the proof by cancellation.

## 2. Where purity is at most one

Thermal purity is the sum of squares of normalized positive Gibbs weights. A spatial ratio is a purity when its base length is even: the normalized even power of the inherited self-adjoint transfer operator has a nonnegative spectrum. Its eigenvalues need not individually be nonnegative before that even power. Thus every ladder edge used here is in (0,1] when all reflected spatial base lengths are even. Subsequent doublings preserve this domain.

This argument is not an assertion that spatial ratios at arbitrary odd base lengths are at most one. Odd target lengths enter only through the inherited signed-transfer interpolation proof, which uses positivity of physical partition functions to identify a positive dominant transfer eigenvalue. No thermal coordinate is silently reinterpreted as a spatial length.

## 3. Separate joint information is compatible with component bounds

Suppose actual canonical purities satisfy A>=a, B>=b, C>=c and A^4 B^2 C>=K, with 0<a,b,c<=1 and 0<=K<=1. These are simultaneous lower inequalities concerning the same actual ladder. They need not be attained simultaneously as equalities. In particular it is valid to have K>a^4 b^2 c. Taking componentwise maxima from multiple proven routes preserves all inequalities, provided each component denotes the same edge at the same base. Taking a maximum of independent full-product lower bounds is equally valid. No optimization over nonexistent exact endpoint tuples is required.

Dropping factors bounded above by one gives

    B^2 C >= K,    (A^2 B)^2 >= K,    C >= K.

For the chain, S^2 T>=K gives T>=K and S>=sqrt(K). These are inequalities, not identities between partial products of different orderings. In particular, full-product order invariance never licenses replacing an order-specific intermediate partition-function denominator by another one.

## 4. Joint-aware canonical continuation

Write G(z)=1-(1-z)^2/(2z^2). On 0<z<=1,

    G'(z)=(1-z)/z^3 >= 0.

The inherited canonical purification step gives actual new lower bounds through G(A^4 B^2 C), G(B^4 C^2 D), G(C^4 D^2 E), successively. Therefore valid improved lower endpoints are

    d = G(max(a^4 b^2 c,K)),
    e = G(max(b^4 c^2,K^2) d),
    f = G(max(c,K)^4 d^2 e).

An output is used only if it is positive. Every argument remains at most one because all factors are certified lower endpoints of purities. Downward rounding at every stage is safe. The chain analogue is

    s_new = G(max(s^2 t,K)),
    t_new = G(max(t,K)^2 s_new).

The new components have the same original order at the fully doubled base. Another independently propagated direction order may provide K_new there. Combining its product information with these component bounds is valid only at this new base. The old K must not be reused there without a separate proof.

Repeated time-first cycles before canonical conversion are valid applications of the same rotating-ladder proof. Transporting at each intermediate even base is also permitted and can supply the finite-window endpoints. A successful late cycle alone does not cover any earlier unbridged size interval.

## 5. Joint-aware one-dimensional window

Let actual canonical S>=s>0, T>=t>0, with S^2 T>=K. Put
p=max(s^2 t,K)>1/2 and define

    w=(1+sqrt(2p-1))/2,
    r=(1-w)/w,
    d=t/(1+r^2),
    I(s,t;K)=(1-r) min(s sqrt(d),d).

The exchange identity gives P_x(n,2 beta) T(n,beta)^2=S(n,beta)^2 T(2n,beta). As T(n,beta)<=1, the left spatial purity is at least the actual S^2 T and hence at least p. The inherited inverse-purity argument therefore bounds its dominant weight below by w and its relative tail above by r. The remainder of the signed transfer interpolation uses the separate lower bounds s,t, yielding exactly I.

Increasing p decreases r. For fixed s,t, both 1-r and d increase, so the entire expression increases. Replacing p by a valid joint bound never invalidates its use with separately supplied, possibly non-sharp, s,t.

Integer-square-root lower enclosures decrease w, increase r and decrease d. A lower enclosure for sqrt(d) then also has the safe direction. The finite window remains every integer n<=M<=2n at inverse temperature beta.

## 6. Joint-aware two-dimensional window

The inherited transverse spatial proof gives

    S_x(n,W;beta) >= A^2 sqrt(2B-1),   m<=W<=2m,

provided the certified b>1/2. Since A^2 B>=sqrt(K), factor the right side as (A^2 B) f(B), where f(B)=sqrt(2B-1)/B. This function is nondecreasing on [1/2,1]. In addition to the derivative check,

    f(y)^2-f(x)^2
      = (y-x)(x+y-2xy)/(x^2 y^2) >= 0

for 1/2<=x<=y<=1 gives an exact rational witness. The complete quotient f is monotone. Considering its numerator and denominator separately would not justify the substitution. Hence

    sx=max(a^2 sqrt(2b-1), sqrt(K) sqrt(2b-1)/b)

is valid. Also B^2 C>=K, so the transverse thermal interpolation gives

    ty=I(b,c;K).

The unchanged outer application gives the valid common lower bound

    T(L,W;beta) >= I(sx,ty;0),
    n<=L<=2n, m<=W<=2m,

on every integer rectangle in that common box. Both calls must satisfy their own inverse-purity margin. The outer call is not given K, since no such outer joint-product inequality has been established.

The scalar code does not establish arbitrary aspect ratios, infinite-volume uniqueness, a physical transition, or optimality of any coupling threshold.

## 7. Model-specific acceptance still required

For each final selected candidate the independent audit must verify:

1. Immutable physical inputs and directed partition-function ratios.
2. Exact order, physical spatial base and inverse temperature for each state.
3. Every time-first/canonical transition, independent joint K and safe rounding.
4. Every finite box before the asymptotic onset, including early repeated-order cycles and odd integer sizes, together with independent smaller-size bounds.
5. The final small-defect theorem and direct exponential witness for each reported rational gap.

This review keeps lemma acceptance and new physical-certificate acceptance separate. Sources and exact supplementary test outputs are in `results/`.
