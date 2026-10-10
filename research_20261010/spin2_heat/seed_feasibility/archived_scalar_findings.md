# Stronger bootstrap audit for the spin-2 campaign

This note separates universal mathematical statements from numerical basin
diagnostics and from statements conditional on the campaign's finite-moment
inputs. No claim of a spin-2 uniform-gap proof is made.

## 1. The scalar squaring inequality is already sharp

For a probability distribution w with purity P=sum(w_i^2)=1-u, squaring and
renormalizing gives P'=sum(w_i^4)/P^2. Consequently

    1-P' <= f(u),       f(u)=u^2/[2(1-u)^2].

For every 0<=u<=1/2, choose a two-point distribution

    w_+= (1+sqrt(1-2u))/2,   w_-=1-w_+.

It has purity 1-u and attains equality. Thus a stronger scalar map based only on
the old purity is impossible in precisely the high-purity regime of interest.
Additional spectral multiplicities, maximal weights, or further moments would
be needed to improve it. The original inequality is not merely a loose estimate.

For arbitrary purity P, squaring also obeys P'>=P. Indeed Jensen applied with
probability weights w_i gives sum(w_i^4)>=P^3. The safe global lower map used in
the exploratory code is therefore G(P)=max(P,1-f(1-P)). Below P=1/2 it reduces to
G(P)=P; a uniform distribution shows why no universal strict improvement is
available there.

## 2. A larger rigorously sufficient symmetric basin

Write p=1-S(n,b), q=1-T(2n,b). The certified diagonal update is

    p' = f(1-(1-p)^2(1-q)),
    q' = f(1-(1-q)^2(1-p')).

Let h(u)=f(1-(1-u)^3). If p,q<=u and h(u)<=u, then p',q'<=h(u).
Moreover

    h(u)=C(u)u^2,
    C(u)=[3-3u+u^2]^2/[2(1-u)^6].

C(u) is strictly increasing: with t=1-u it equals
(t^-1+t^-2+t^-3)^2/2. Hence u*C(u) is strictly increasing, starts at zero,
and has a unique positive crossing of 1. Denote that crossing by u_*.

    0.1273107863645776 < u_* < 0.1273107863645777.

The bracket is verified by exact rational arithmetic in certify_scalars.py.
For every u_0<u_*, h(u)<u on (0,u_0], and iteration converges to zero. Thus

    S(n_0,b_0)>0.872689213635422398...,
    T(2n_0,b_0)>0.872689213635422398...

are sufficient, with strictness interpreted through 1-u_* (the displayed decimal
alone should not be used as a rigorous endpoint). Both purities >=7/8 are a
particularly convenient rational sufficient condition. At u_0=1/8,

    C(u_0)=913952/117649 = 7.768463820346964... < 7.9,

so the conservative recurrence u_next=7.9*u^2 has r=7.9/8=79/80<1.
It yields a uniform gap bound log(80/79)/b_0 using the standard length interpolation.

The sharper asymptotic rate log[1/(C(u_0)u_0)]/b_0 follows from the same recurrence;
to assert that bound for every starting length, retain the finite prefactor in
the Gibbs-weight estimate or first perform finitely many startup rounds. The
0.99 / C=5 theorem remains a simple clean all-length formulation.

## 3. Asymmetric starting pairs

The update is coordinatewise monotone wherever it is valid. Its convergence
basin is a downward-closed subset of the (p,q) square. An exact characterization
of this sufficient-method basin is the union, over finite k, of inverse images
under k updates of the open square max(p,q)<u_*: entry implies convergence, and
any convergent sequence eventually enters that square.

Exact rational, upward-rounded iterations certify the following entries into
max(p,q)<=0.01:

| p upper | q upper | Number of updates |
|---:|---:|---:|
| 0.125 | 0.125 | 5 |
| 0.1273 | 0.1273 | 10 |
| 0.000000007243 | 0.2 | 7 |
| 0.01 | 0.197 | 7 |
| 0.1 | 0.15 | 7 |
| 0.2 | 0.032 | 7 |

The diagnostic floating search locates the limiting q near 0.2006145124 when
p=0; near p=0.1 it locates q near 0.1505998634. These are not certified boundary
values and should not be advertised as sharp necessary conditions for the model.
They are boundaries of a sufficient scalar method, not of the set of gapped
Hamiltonians.

In particular, arbitrarily high spatial purity does not make the original
method work with arbitrary thermal purity. With near-perfect spatial purity,
this map still needs thermal purity roughly above 0.7994.

## 4. Anisotropic search

Writing the state as lower bounds (s,t) for (S(n,b),T(2n,b)), the following
rectangular moves are valid consequences of the same exact identities:

    temperature-only: (s,t) -> (s^2*t, G(t)),
    space-only:       (s,t) -> (G(s), t^2*G(s^2*t)),
    diagonal:         (s,t) -> (G(s^2*t), G(t^2*G(s^2*t))).

basin_search.py propagates all nondominated states on a grid allowing up to
seven independent space doublings and seven temperature doublings. In 45 tested
points immediately outside the diagonal basin, this search found no successful
anisotropic path. This is an explicit finite negative search, not a proof that
all anisotropic schedules are equivalent or that other moment inputs cannot help.

For an integer power k>=2, one further generic estimate is

    1-P_k <= 2^(1-k) u^k/(1-u)^(2k-2),

where P_k is the purity after taking each weight to power k and normalizing.
Proof: bound sum_{i<j}(w_i*w_j)^k by (sum_{i<j}w_i*w_j)^k and use
sum_i w_i^k>=P^(k-1). This higher-power bound is valid, but does not supply
the missing cross-temperature thermal information by itself.

## 5. High spatial purity alone cannot force thermal concentration

Take an onsite product model H_L=sum_j h_j. With z(b)=tr exp(-b*h),

    Z_L(b)=z(b)^L,
    S(n,b)=1,
    T(L,b)=[z(2b)/z(b)^2]^L.

The spatial transfer operator is rank one and exactly self-adjoint. Nevertheless,
for h=0 on a d-dimensional site, T(L,b)=d^-L at every b. Thus spatial purity alone
cannot imply ground-state uniqueness, or eventual thermal concentration, even
with an exact transfer representation. Choosing a unique onsite ground state
with arbitrarily small gap delta likewise shows that S=1 gives no positive
quantitative gap lower bound independent of additional input.

This counterexample concerns the inference from S alone. It does not imply
anything negative about the actual spin-2 Heisenberg gap.

## 6. Can retaining the denominators help the current spin-2 starting point?

The identities before discarding denominators are

    S(n,2b)=S(n,b)^2*T(2n,b)/T(n,b)^2,
    T(4n,b)=T(2n,b)^2*S(2n,2b)/S(2n,b)^2.

Useful upper bounds A>=T(n,b), B>=S(2n,b) improve the corresponding lower
estimates by dividing by A^2 or B^2. In particular, a tiny *upper* bound on
T(n,b) could greatly improve the space-purity propagation. This is a real
possible improvement over replacing every denominator by 1.

However, at the campaign's b=2.25 candidate the thermal-step denominator is
already essentially 1. Conditional on the independent audit's rounded bounds

    S(256,2.25)>=1-7.243e-9,
    T(512,2.25)<=7.072e-17,

the sharp squaring inequality gives

    S(512,2.25)>=1-2.623052488e-17.

Hence retaining 1/S(512,2.25)^2 changes a bound by at most

    1+5.246104976e-17.

Using the exact second identity and S(512,4.5)<=1 gives the upper bound

    T(1024,2.25)<5.002e-33.

All scalar comparisons here were checked with exact rationals. Thus retaining
this denominator cannot remedy the current thermal-purity failure; enlarging
the chain at this fixed temperature makes thermal purity still smaller.

This does NOT rule out startup at a larger inverse temperature. For example,
spatial moment information at b=4.5 and b=9 could provide a new thermal bound
at b=4.5. Neither the sharpness result nor the low-temperature audit says that
the true spin-2 Gibbs purity cannot become large at an appropriately larger b.

## Reproduction

    python basin_search.py
    python certify_scalars.py

basin_results.json contains the floating diagnostics. scalar_certificates.json
contains exact rational startup records and the conditional denominator checks.
