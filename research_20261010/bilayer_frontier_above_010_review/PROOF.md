# Independent physical and all-size audit above g=0.10

Updated 2026-10-10 18:39 EDT / 22:39 UTC.

## Accepted discrete points

For the ordinary spin-1/2 periodic square bilayer, unit rung coupling, equal intralayer coupling g in both spatial directions, no crossed inter-rung bonds, and the existing positive-neighbor multiedge convention at side two:

- g=1001/10000: gap >= .054499712024
- g=201/2000: gap >= .049244008353
- g=101/1000: gap >= .040917096762
- g=203/2000: gap >= .029199965244
- g=51/500: gap >= .016509932002

Each bound holds for every integer square side L>=2 and implies a unique finite-volume ground state. These five points alone do not certify intervening real couplings. No physical-gap monotonicity or phase-boundary conclusion is used.

## Exactly what is inherited and what is new

The Hilbert-space model is H'=H+3N/4=Q+gV, equivalently Q+(g/2)A in the stored integer convention. The trial metric and fixed integer basis vectors do not depend on physical g. Previously accepted physical matrix identities, the full residual polynomial of the 8x4 fixed vector, and translated odd-family structural polynomials are pinned to independent review manifests in PROVENANCE.json. They are operator-polynomial identities for all real g; they are not numerical interpolation of successful gap points.

This audit does not repeat the expensive physical contraction that established those identities. It independently contracts the pinned 4x4 Gram/first/complete-second-moment matrices with the saved 11-component vector, and the pinned 8x8 Gram/affine operator matrices with the saved 43-component numerator vector. For the 8x4 denominator it matches the 43-component vector, norm, mean and complete quadratic second moment against the independently reconstructed accepted fixed-vector polynomial. That polynomial includes the full q=8 residual contribution established by the signed commutator method. It is not a projected residual or an assumed zero leakage.

All three vectors must equal the witnesses in the last accepted [0.09,0.10] interval record. Norms are positive. Every supplied affine mean and complete quadratic variance is reproduced exactly. The identity v(g)=<H'(g)^2>-<H'(g)>^2 is verified coefficientwise, with v0>=0, v2>=0 and 4v0v2-v1^2>=0. Thus the variances are globally nonnegative and convex. New physical-coupling endpoints, all cutoffs, all thermal sums and short-size inequalities are recalculated, rather than inherited from a g<=0.10 certificate.

The denominator search dimensions remain 11 and 43, with retained spectral counts 49 and 97. The 8x8 numerator uses one retained Rayleigh contribution from a 43-dimensional search. Its physical size is 128 spins and full Hilbert dimension 2^128. These three types of dimension are not interchangeable.

## Fixed odd family, reconstructed independently

The literal family is w_r(z)=u_r+z v_r, with Q u_r=u_r, Q v_r=3v_r and z fixed to 1/10. Its physical metric is independent of g. Accepted displacement arrays G(z),A(z),B(z) encode <w,w>, <w,H'(z)w> and <H'(z)w,H'(z)w> with degrees at most 2,3,4. Those degree bounds follow from the affine operator and affine vectors. Prior exact source-point matches supplement the identities rather than justify extrapolation.

Write G(z)=G0+z^2 G2 and define

 Qmom=G0+3z^2 G2, Q2mom=G0+9z^2 G2,
 Vmom=(A-Qmom)/z=v0+z v1+z^2 v2,
 Cmom=2v0+4z v1+6z^2 v2,
 Dmom=(B-Q2mom-z Cmom)/z^2.

All divisions are exact polynomial identities. The mixed weights 2,4,6 come from the sum of left/right Q eigenvalues; no equality of the two potentially complex QV and VQ cross terms is presumed. At arbitrary physical coupling g and fixed z:

 A_fixed(g)=Qmom+g Vmom,
 B_fixed(g)=Q2mom+g Cmom+g^2 Dmom.

The reviewer evaluates these identities at z=1/10 and independently Fourier-transforms every displacement array in exact Q(sqrt(2)). All 16 and 32 momentum Grams are strictly positive. Division by each Gram reproduces every affine mode mean, complete quadratic second moment and full variance. The exact quadratic-field covariance test verifies nonnegative convex variance. Directed sqrt(2) enclosures account for the sign of its coefficient. Every saved endpoint enclosure, Temple denominator, width and correlated relative endpoint matches exactly. Across the five points this checks 240 momentum modes, with spin multiplicity three separately preserved.

The frozen point records mistakenly label odd_band.fixed_center by the physical point g. Their numerical Gram and moment coefficients actually use z=1/10. The producer's separately hashed METADATA_ERRATUM.json explicitly corrects this. The reviewer first requires the exact documented stale label, then changes only an in-memory copy to z=1/10 before independently reconstructing its coefficients. No frozen producer file is modified. The point certificate is accepted with this explicit metadata correction, not by treating the incorrect label as a correct assertion.

## Stable comparison and complete counted low band

The independently proved oscillator comparison is valid throughout 0<=g<1/4, beyond the old 0.10 frontier. Put alpha=1-2g and delta=sqrt(1-4g)>0. For the 4x4 and 8x4 simple periodic graphs, the bosonic vacuum creation norm is v=3Ng^2/2. The reference ground shift satisfies

 E_b=-v/(alpha+delta)=(3N/8)(2g-1+delta),
 r_q(g)=(3N/8)(2g-1)+(3N/8+q)delta.

Ordered min-max after hard-core compression gives reference multiplicities d_q=binom(3N+q-1,q). In particular the second physical eigenvalue is at least r1 and ordered level 3N+2 is at least r2. This is a whole-Hilbert-space statement, not a magnetization-sector assumption.

At every new point, the audit checks r1-rho_ground>0 and r2-rho_ground>0 with lower square roots. The first condition identifies a unique global ground state below r1; the even trial has positive overlap with it. It also checks r2-theta_k>0 for every odd momentum mode. The even ground and all 3N odd trial directions are mutually orthogonal by parity, momentum and spin symmetry. They span 1+3N directions strictly below r2; the counted comparison permits at most 1+3N eigenvalues there. Consequently there is exactly one low even ground state and one low state in each odd momentum/spin sector, and every next level in each such sector lies at or above r2. This supplies the Temple denominators without discarding any possible extra low state.

For a point or a closed range [a,b], r_q(g)-rho(g) and r2(g)-theta_k(g) are concave because their only nonlinear term is a positive multiple of sqrt(1-4g). Their minima are bounded by endpoint minima. Complete variances are convex, so endpoint maxima are safe. Each Temple lower endpoint therefore follows from its complete variance divided by a strictly positive, independently checked denominator.

After retaining one ground and 3N odd levels, every omitted physical eigenvalue is covered by q=2,...,N with multiplicities binom(3N+q-1,q). The exact count identity sum_(q=0)^N d_q=binom(4N,N)>=4^N is checked. Positive excess reference terms only weaken the upper bound. Physical binomial counts binom(N,q)3^q are not substituted for these oscillator counts.

## New temperatures, ratios and short-size bridges

For each denominator and each of its required temperatures, the reviewer independently upper-bounds the normalized ground term, all 3N retained odd contributions and the complete counted omitted tail using directed rational exponentials. All supplied trace terms must be at least these independent bounds. The large numerator remains one exact Rayleigh contribution; no claim that the trial is an exact eigenstate is needed.

Correlated affine energy combinations are independently rebuilt with weights (8,0,-2), (16,0,-4) and (0,4,-2) for J1,J2,C0. Additive extensive shifts cancel exactly. Dividing an exponential lower bound by each complete trace upper power verifies all three saved initial joint/spatial ratios.

For every point, the short-side L=2,...,7 bounds are recalculated at the actual new g:

 gap_L >= C_L(2g-1)+(C_L+1)sqrt(1-4g),
 C_L=3S_L/16, S_L=(16,18,32,50,72,98).

The L^2 physical rung counts and side-two edge multiplicities are checked. All six bounds are positive. Reusing the old g<=0.10 short gap would not have been valid here.

The independent scalar implementation then checks initial txy purities, order transport, joint/canonical continuation, every physical geometry/temperature label, every intervening finite integer box, every strict thermal gap witness and the terminal small-defect witness. Together with L2,...,7, these cover all integer square sides without a gap. The new physical audit is a required precondition for this scalar replay.

## Legal-domain claim and limitations

The additional physical-gate domain is independently verified as the closed interval

 [1/10,129259642269/1073741824000].

Every ground, even and odd margin is positive at both endpoints. Concavity establishes the same throughout. The fixed Grams and globally positive variance polynomials stay valid independently of g. The short L7 comparison has opposite signs across

 [129259642269/1073741824000,64629821209/536870912000],

near 0.120382423. Its derivative is 2C-2(C+1)/sqrt(1-4g)<0 for g>=0, so this brackets the limiting zero for this particular complete short-bridge method. All nine saved cutoff root brackets and all listed margins at g=.11 and the legal upper endpoint are independently checked. This is a physical-input legality domain, not an all-size gap certificate on that whole range. A failed bounded temperature scan is not an all-temperature obstruction.

## Reproduction and tests

No producer code is executed or imported. Mathematical reuse is limited to hash-pinned functions from accepted independent reviews, with exactly documented changes: fixed trial center z=1/10 and allowing a new-coupling singleton in the scalar domain. Ground and numerator contractions, reference formulas, complete trace sums, short-size checks and legal-domain checks are independently implemented here.

Nine adversarial physical corruptions are rejected: changed fixed vector, incorrect odd Gram, incorrect mode mean, missing odd mode, altered full variance, optimistic cutoff, omitted thermal tail, altered short-size gap and inflated initial ratio. Both the main audit and fresh-directory replay use CPU 4, no more than 600 CPU seconds and 700 MiB address space per batch. Typical cost is 10 seconds and 20 MiB. All outputs stay in this separate review; no root, producer or GitHub state is changed.

For the domain-wide short-size assertion, C_L<=C_7 and (2g-1)+sqrt(1-4g)<=0 for g>=0. Hence every other stated short-size lower bound is at least the L7 bound. Endpoint positivity and the L7 derivative therefore cover the whole specified short-size family, not just one size.
