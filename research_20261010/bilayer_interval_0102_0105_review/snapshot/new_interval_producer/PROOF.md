# Fixed-witness closed bilayer extension from .102 to .105

2026-10-10 23:03 UTC / 19:03 America/New_York. Exact producer candidate pending independent physical-polynomial and all-size scalar review.

Six adjoining closed intervals of width1/2000 cover every real g in[51/500,21/200]. Their candidate all-integer periodic-square bound is

 gap >= 17785998829/10^12 = .017785998829,

with a unique finite-volume ground for every integer L>=2. The minimum occurs on[.102,.1025]. This is uniform closed-interval control, not interpolation between successful point gaps.

Joining the previously reviewed66-interval[0,.10] continuation and eight-interval[.10,.102] extension would preserve

 gap >= 4499695659/10^12 = .004499695659

for every real0<=g<=.105, across80 closed intervals, conditional on acceptance of this new package and its two complete residual inputs. The g=.105 point has its separate stronger candidate .031673112867; the point and interval statements must not be conflated.

## Fixed physical witnesses

Use the new16D4x4 and43D8x4 optimized .105 vectors, with the complete residuals in their separately frozen physical packages. Use the one-state .105-optimized43D8x8 numerator. No witness is changed as g varies through this interval. Both odd trial families are fixed atz=.1 and correctly labeled as such in every record.

Denominator retained counts remain49/97, while ground search dimensions are16/43 and total ground-plus-odd trial dimensions64/139. Largest numerator search dimension43, retained count1, physical Hilbert dimension2^128. No new support contraction, larger trial space or full ED is performed in this extension.

## Exact full-moment polynomial export

H'(g)=Q+(g/2)A. The fixed-vector mean is affine and its full second moment is

 <H'(g)^2>=<Q^2>+(g/2)<QA+AQ>+(g^2/4)<A^2>.

The existing accepted basis is B,L,U=R+M, where B has q0/q2, L and R have q4, and M has q6. The accepted exact Gram blocks give Q and Q² expectations by these triplet-number weights. For QA+AQ, each exact A-block is multiplied by the sum of the two relevant triplet numbers. Thus Bpair-L and Bpair-R carry6, L-L/R-R carry8, R-M carry10, and M-M carries12. The vacuum-pair block uses its exact q0+q2 weight. All coherent R/M cross terms are retained.

The accepted exact geometry matrices F,S,V,W,X,Y,Z implement these blocks. Given the newly computed COMPLETE second moment at nonzero g*=21/200, recover <A²> algebraically from the displayed identity. No component is omitted and no projected second moment is substituted. This extends the full fixed-vector variance polynomial exactly to all real g, not merely near the source point.

export.py performs this construction separately for16D and43D, verifies exact reproduction of each .105 mean/complete variance, verifies symmetric QA+AQ blocks, and checks the variance quadratic is positive semidefinite (v0>=0,v2>=0,4v0v2>=v1²). All unnormalized expectations and exact coefficients are saved. The two polynomial exports depend explicitly on the frozen physical residuals and their exact basis/geometry sources.

## Uniform physical interval inequalities

For each closed interval[a,b], the fixed means are affine, complete variances are convex quadratic, and the stable bosonic reference

 r_q(g)=(3N/8)(2g-1)+(3N/8+q)sqrt(1-4g)

is concave. Minimum endpoint values of r_q-rho and r2-theta_k therefore give uniform lower cutoff margins; maximum endpoint complete variance gives a uniform upper variance. Exact rational/Q(sqrt2) enclosures are used. Separately check r1-rho>0, r2-rho>0 and EVERY odd-mode cutoff. This establishes global ground identification, sector Temple bounds and the49/97 level counts uniformly.

The full denominator trace retains the ground, every odd mode and all omitted reference shells q2,...,N with multiplicities binom(3N+q-1,q). The numerator is one Rayleigh contribution. Correlated energy combinations for J1,J2,C0 are affine; endpoint minima are taken before exponentials. No physical-gap monotonicity is assumed.

Each short L2,...,7 bound is recalculated at the interval upper endpoint using C_L(2g-1)+(C_L+1)sqrt(1-4g). Its derivative is negative on this range, so the endpoint bound holds throughout the interval.

## Scalar, integer coverage and reproduction

Five fixed proposal temperatures8,9.4,9.5,10,11 are tested; every selected interval uses9.4. Exact replay recalculates traces, initial purities, joint ratios, order transport, every needed direct2D finite window, the canonical terminal exponential witness and all six short-size comparisons. Each record has physical basepoints/temperature labels and a complete all-integer path. Summary verifies exact closed-interval adjacency and endpoint coverage.

CPU3, one thread,600CPU-second/700MiB caps. The six-interval pass took2.94 seconds. Reproduction checks all seals, regenerates polynomial exports into separate check files, replays six intervals into a separate check directory, and compares exact results without changing frozen files. No remote changes are made.
