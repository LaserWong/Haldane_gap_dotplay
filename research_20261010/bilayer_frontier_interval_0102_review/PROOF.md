# Independent continuous extension through g=0.102

Updated 2026-10-10 18:42 EDT / 22:42 UTC.

## Accepted result

For the ordinary periodic spin-1/2 square bilayer, unit rung exchange, equal straight intralayer couplings g in both directions, no crossed inter-rung interactions, and the accepted positive-neighbor multiedge convention at side two:

- Every real g in [1/10,51/500] has gap >=13574634391/10^12=.013574634391.
- Combining this with the separately accepted [0,1/10] result gives gap >=4499695659/10^12=.004499695659 for every real g in [0,51/500].

Both statements hold for every integer square side L>=2, with a unique finite-volume ground state. The new union has 74 closed parameter pieces. The conclusion is uniform on the full real intervals, not just on grid points or endpoints. No monotonicity of the physical gap in g is assumed.

## Reused independent physical verifier

The point-frontier independent review established operator-polynomial validity and positive physical gates for the fixed ground/numerator witnesses and the fixed odd family at z=1/10. Its sealed audit.py is copied byte-for-byte as physical_library.py, and its exact mathematical/input hashes are verified before execution. The complete point proof and acceptance are retained in snapshot. The physical_library does not import or execute producer code.

This inheritance supplies genuine fixed-basis identities for the full moments, rather than a polynomial fit to successful gap certificates. The actual interval audit still recalculates all new endpoint inequalities, complete normalized thermal upper bounds, short-size bridges and scalar continuation. It does not infer interval acceptance from the previously checked discrete points.

The fixed ground vectors have search dimensions 11 and 43. Their complete second moments include all leakage; the 8x4 vector's full q=8 residual contribution is inherited from its independently established signed commutator identity. The numerator is one retained Rayleigh contribution in the 43-dimensional 8x8 space, on 128 physical spins with full Hilbert dimension 2^128. The same explicit integer vectors must be used at both endpoints and throughout each interval.

All interval records correctly label odd_band.fixed_center=1/10. The stale point label and its explicit erratum are kept only in the inherited point package. No such label correction is needed for the new interval records.

## Uniform ground-state inequalities from both endpoints

For each denominator, fixed-vector contraction gives an affine mean rho(g)=rho0+g rho1 and a complete variance v(g)=v0+g v1+g^2 v2. The exact coefficient identities are checked again for every interval. The covariance inequalities v0>=0, v2>=0 and 4v0v2-v1^2>=0 prove nonnegative variance for all real g; v2>=0 proves convexity. Therefore on [a,b],

 v(g)<=max(v(a),v(b))=:V.

For the 16- and 32-rung denominators, the whole-space stable oscillator comparison remains valid on 0<=g<1/4:

 r_q(g)=C(2g-1)+(C+q)sqrt(1-4g), C=3N/8.

The coefficient C+q is positive. Thus r_q-rho is concave on the physical interval, and

 r_q(g)-rho(g)>=min(r_q(a)-rho(a),r_q(b)-rho(b)).

Directed lower square-root enclosures at each endpoint give certified endpoint lower values. Concavity of the exact function then puts every interior value above the smaller certified endpoint lower bound. Concavity is not asserted for the rounded numerical function itself.

Every endpoint ground-identification margin for q=1 is positive. Every q=2 even Temple denominator is positive. The ground lower bound rho(g)-V/m2 follows uniformly. The audit recomputes both endpoints and requires each saved margin, variance maximum and Temple width to equal the independent result.

## Uniform odd-band inequalities and completeness

For each momentum mode, the reviewer reconstructs the fixed-z=1/10 displacement moments and Fourier symbols in exact Q(sqrt(2)). Every Gram is positive. This yields affine theta_k(g), a complete quadratic second moment and a globally nonnegative convex full variance v_k(g). The mixed QV/VQ terms retain their correct 2,4,6 weights; no equality of the two cross terms is assumed.

For each of the 48 distinct momenta across the two denominator patches, evaluate both endpoints with directed sqrt(2) enclosures. Since r2(g)-theta_k(g) is concave, its endpoint minimum m_k is a uniform positive lower bound. Since v_k(g) is convex, its endpoint maximum V_k is a uniform upper bound. Finally theta_k(g)-rho(g) is affine, so its minimum is bounded by the endpoint minimum. Consequently

 lambda_k(g)-rho(g) >= min_endpoints(theta_k-rho)-V_k/m_k

throughout each interval. All endpoint enclosures, margins, maxima and relative lower endpoints are compared exactly. The review checks 384 momentum-mode interval certificates, including both endpoints. Additional interior rational evaluations inherited from the verifier are diagnostics; the concavity/convexity argument is what covers every unsampled real coupling.

The complete counting argument is unchanged and remains applicable because every mode and the even ground lie strictly below r2 throughout the interval. They provide 1+3N mutually orthogonal low directions. The global oscillator comparison places ordered level 3N+2 at or above r2, leaving exactly those 1+3N low levels and no omitted low sector. Sectorwise Temple bounds are therefore legitimate. The omitted thermal tail uses q=2,...,N and multiplicities binom(3N+q-1,q), with total count binom(4N,N)>=4^N. Spin multiplicity three and the retained counts 49/97 are explicitly checked.

## Uniform thermal inputs and short sizes

The normalized trace upper is the sum of its verified ground term, all retained odd terms and the complete counted tail. Uniform Temple widths and relative eigenvalue endpoints enter directed exponential upper bounds at each required temperature. Every saved component must dominate the independent recomputation.

The three numerator/denominator energy combinations are affine in g. Their exact coefficient weights are (8,0,-2), (16,0,-4) and (0,4,-2); extensive shifts cancel. Taking each affine minimum at the two endpoints gives a uniform exponential lower bound. Combining these with the complete trace upper powers yields valid uniform J1,J2,C0. This handles correlations algebraically, without requiring simultaneous saturation of separate bounds.

For short sides L=2,...,7, the lower bound is recomputed at the upper coupling endpoint b:

 f_L(g)=C_L(2g-1)+(C_L+1)sqrt(1-4g),
 C_L=3S_L/16, S_L=(16,18,32,50,72,98).

Its derivative is 2C_L-2(C_L+1)/sqrt(1-4g)<0 for g>=0. Thus f_L(g)>=f_L(b)>0 throughout[a,b]. This is monotonicity of the explicit comparison function, not of the physical gap. Both small-size geometry and every saved bound are checked.

## Size continuation and real-parameter coverage

Every certified initial triple is based at spatial square 8 and physical beta twice beta_initial. Raw time-first and canonical ladder bounds, exact order conversion, joint products and every edge/base/temperature label are verified by the accepted independent scalar implementation.

The finite-window direct lemma covers every integer side in each successive doubled box, including odd sizes. Each saved thermal purity and finite gap is checked by a strict rational exponential witness. The terminal canonical small-defect state is checked at its actual beta, with 0<u<=1/500 and exp(beta*gap)*32u<1. Each reported per-interval gap is the minimum of every required finite window, all six short-size bounds and the terminal asymptotic bound. Missing windows, incorrect terminal coordinates and wrong labels are rejected.

Eight saved closed intervals meet exactly at 401/4000,201/2000,403/4000,101/1000,81/800,203/2000 and407/4000. They begin 1/10 and end 51/500. The minimum accepted interval gap is .013574634391, attained on [407/4000,51/500]=[.10175,.102]. The prior independently accepted [0,.10] uniform lower bound is .004499695659; its acceptance and manifest are hash-matched. Taking the minimum produces the stated uniform union bound on [0,.102].

## Validation and reproducibility

The producer interval seal is ae11e04adf4aded2a5aebd57bdc3692a0a2c3e6023ed060740bf93e16efa42e6. The prerequisite independent point seal is d101b554ea00c044e148031ec4d073d10f6f757b78a019e5bc6502a67e086d05. The prerequisite prior-union seal is c9dadb17430a3523cda109599f3025ff62c7b9ebebacc2b9eb48acce2381e977.

Eight adversarial changes are rejected: wrong actual fixed z, changed endpoint variance, changed endpoint ground margin, changed odd endpoint enclosure, inflated uniform energy combination, altered short-size bound, wrong terminal beta and a missing finite window. The exact full audit is repeated in a fresh directory and substantive outputs must agree. Each run uses CPU 4, at most 600 CPU seconds and 700 MiB address space, about 9 seconds and 25 MiB in practice. No large physical contraction, eigensolver, producer edit, root update or GitHub write is performed.
