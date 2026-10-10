# Correlated axis orders with exact transport to a canonical staircase

2026-10-10 14:17 America/New_York / 18:17 UTC.

These are new g=3/50 candidates. Their physical input and new scalar records
require independent review. The two transfer representations, sequential
arbitrary-order update, and adjacent-swap lemma were independently checked in
`../../general_dimension_review/PROOF_REVIEW.md`, Sections 1–3. This note makes
the geometric specialization explicit instead of relabeling measured purities.

## 1. General correlated first cycle

Let v=(n,n,beta), let D_x,D_y,D_t double the indicated coordinate, and write
P_i(v)=Z(D_i v)/Z(v)^2. Let (i,j,k) be any permutation of x,y,t and set

    v0=v, v1=D_i v, v2=D_j D_i v, v3=D_k D_j D_i v.
    q1=P_i(v0), q2=P_j(v1), q3=P_k(v2).

All spatial lengths are even, so every ratio is a purity in (0,1]. Define

    J1=Z(v3)/Z(v0)^8 = q1^4 q2^2 q3,
    J2=Z(v3)^2/Z(v1)^8 = q2^4 q3^2,
    C0=Z(v3)/Z(v2)^2 = q3,
    G(z)=1-(1-z)^2/(2z^2).

The exact exchange identities and the one-coordinate squaring bound give

    a >= G(J1),
    b >= G(J2 a),
    c >= G(C0^4 a^2 b).

After these three sequential updates, (a,b,c) bounds the ordered (i,j,k)
staircase at the common basepoint v3=(2n,2n,2beta). The three values are not
automatically a canonical x,y,t staircase.

For the 4x4,8x4,8x8 seed family, n=4. Rotations of the square model identify
Z(n,2n;b)=Z(2n,n;b). Therefore:

| order | J1 | J2 | C0 |
|---|---|---|---|
| x,y,t | Z(8,8;2b)/Z(4,4;b)^8 | Z(8,8;2b)^2/Z(8,4;b)^8 | Z(8,8;2b)/Z(8,8;b)^2 |
| x,t,y | Z(8,8;2b)/Z(4,4;b)^8 | Z(8,8;2b)^2/Z(8,4;b)^8 | Z(8,8;2b)/Z(8,4;2b)^2 |
| t,x,y | Z(8,8;2b)/Z(4,4;b)^8 | Z(8,8;2b)^2/Z(4,4;2b)^8 | Z(8,8;2b)/Z(8,4;2b)^2 |

Every numerator uses the complete retained low-band trace lower bound. Every
denominator uses the complete heat-trace upper bound, including all omitted
number-sector bins. Energy shifts are canceled explicitly in the code; they are
not silently assumed to be extensive.

## 2. Adjacent swaps and their basepoints

At any current basepoint w, suppose a=P_i(w), b=P_j(D_i w). In the swapped
ordering write c=P_j(w), e=P_i(D_j w). Cancellation gives

    e c^2 = b a^2.

Since c,e<=1, valid lower bounds for the swapped pair are

    c >= a sqrt(b),       e >= a^2 b.

The prefix before the pair is unchanged, and the endpoint after the pair is
unchanged because D_i and D_j commute. Thus all later staircase values retain
their original basepoints. Downward square-root rounding preserves the bounds.

After an x,t,y cycle at v3, the bounds mean

    a <= P_x(v3), b <= P_t(D_x v3), c <= P_y(D_t D_x v3).

Swap the adjacent t,y pair. This produces the canonical lower triple

    (A,B,C) = (a, b sqrt(c), b^2 c)

at the same v3, where the entries bound P_x(v3), P_y(D_x v3), and
P_t(D_y D_x v3), respectively.

After a t,x,y cycle the bounds mean

    a <= P_t(v3), b <= P_x(D_t v3), c <= P_y(D_x D_t v3).

First swap t,x, obtaining (a sqrt(b), a^2 b, c) with order x,t,y. Then swap
t,y to obtain the canonical triple

    (A,B,C) = (a sqrt(b), a^2 b sqrt(c), a^4 b^2 c).

Again, the canonical basepoint is exactly (8,8,2beta). The physical temperature
coordinate is not interchanged with a spatial coordinate in the interpolation
theorem. Only justified lower bounds are transported between staircase paths.

## 3. Exact arithmetic and numerical candidates

`transport_orders.py` evaluates all ratios with the directed-dyadic exponential
routine, rounds every new purity downward, encloses each square root by an
integer-square-root inequality, and then invokes only the previously reviewed
canonical x,y,t recursion and its canonical all-integer interpolation theorem.

The first-order full-band moments at g=3/50 give:

| transported order | initial beta | canonical replay gap | direct scope |
|---|---:|---:|---|
| x,t,y | 221/20 | 0.082067113439 | all integer square sides L>=16 |
| t,x,y | 203/20 | 0.099555868340 | all integer square sides L>=16 |

The stronger canonical triple at n=m=8, beta=203/10 is exactly

    A = 499520977455059221 / 500000000000000000,
    B = 498024228182534247 / 500000000000000000,
    C = 198422505485447151 / 200000000000000000.

The finite window 8<=L<=16 can use the already proved canonical signed-transfer
interpolation directly on this triple. Sizes 2<=L<=7 can instead use the number
q>=1 compression bound lambda_2>=a1 and the singlet product Rayleigh bound
lambda_1<=0. These additional bridge computations are saved separately.

The bounded canonical-only scan does not prove that every possible canonical
seed must fail at g=.06. Conversely, successful untransported floating txy/xty
scores were not treated as certificates. The records here use actual bound
transport and canonical replay before making a numerical gap claim.
