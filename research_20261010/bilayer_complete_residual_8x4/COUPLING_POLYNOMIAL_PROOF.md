# Exact fixed-vector coupling polynomials

This separately frozen addendum does not change the physical point seal. No interval result is claimed.

The fixed basis B,L,R,M is coupling-independent, and the saved rational vector is fixed. For H'(g)=Q+(g/2)A, its mean is affine and its complete second moment is quadratic. The point's complete second moment therefore supplies the only additional A² expectation once Q² and QA+AQ are known exactly. This is an operator identity, not polynomial fitting.

In the (B,L,Ufam=R+M) basis, let Qb=diag(0,2,...,2) Gb. The exact Q and Q² blocks are

    Q: BB=Qb, LL=4F, LU=4S, UU=4V+6W;
    Q²: BB=2Qb, LL=16F, LU=16S, UU=16V+36W.

Unlisted off-diagonal B/L,U blocks vanish. Let Ab=(Hb-Qb)/t at t=1/20. Then the anticommutator QA+AQ has

    BB_ij=(q_i+q_j) Ab_ij,
    BL=6Fe, BU=6Se, LL=8S,
    LU=8V+10W,
    UU=8X+10(Y+Y*)+12Z.

Fe and Se prepend a zero vacuum row. Each factor is the sum of occupation numbers of the two sectors connected by that A matrix element; in particular the U/U split treats its q4 and q6 components separately.

For the fixed coefficient vector c, compute q=<Q>, a=<A>, q2=<Q²>, qa=<QA+AQ>, with expectations initially unnormalized. The complete physical point norm at t0=1/20 gives

    a2 = [<H'(t0)²>-q2-t0 qa]/t0².

Then for every real g,

    <H'(g)>/norm = q/norm + g a/(2norm),
    <H'(g)²>/norm = q2/norm + g qa/(2norm) + g² a2/(4norm).

Subtracting the square of the affine mean yields the exact full variance polynomial. `export_polynomials.py` saves all unnormalized expectations, norm, and normalized coefficients in ascending powers of g. It reproduces the exact .10 mean and complete variance. This export uses no new Hamiltonian action or q8 enumeration. A continuous-coupling gap still requires uniform cutoff/count and scalar/finite-window verification.
