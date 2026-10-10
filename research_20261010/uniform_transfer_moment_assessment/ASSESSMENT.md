# Uniform spin-1 transfer moments: bounded assessment

2026-10-10 18:14 EDT / 22:14 UTC. Producer calculation; independent review pending.

## Result

The archived inputs support a rigorously directed, inexpensive refinement of transfer spectral caps and new explicit upper traces at arbitrary even lengths at beta=21/2. They do not, with the tested fixed D26 numerator and cooling-only initialization, certify a smaller seed. No new many-body spectrum, heat trace, MPS contraction, gap, or all-size theorem was computed. The old audited gap statement remains separate.

The rational replay yields:

- trivial sector: |lambda| < 1.002405557347 (old cap 1.00245);
- one complex sector: |lambda| < 0.701394814709 (old proof used its tenth moment directly);
- vector multiplicity space: |lambda| < 0.886398506317 (old cap 0.88643);
- Z24(21/2) <= 1.238492320537;
- Z48(21/2) <= 1.131484383792.

Rounded decimals above are outward displays; exact rationals and every comparison are in results.json. replay.py finishes in roughly 1.2 CPU seconds and 11 MiB resident memory, on CPU0 with a 1 GiB address-space ceiling. It only reads archived files and writes this folder.

## Physical identification and archived premises

The Hamiltonian is the uniform spin-one periodic Heisenberg chain H_L=sum S_j dot S_(j+1), bilinear coefficient one. The shift is a=700741/500000. Every input is Tr exp[-(21/2)(H_L^g+aL)] at L=6,8,10. Here g=I,P,C denotes seam rotations theta=0,pi,2pi/3. The nine files are heat_trace/results/A_L{L}_{twist}_full/certificate.json. Physical dimensions are 729,6561,59049 respectively. P is a seam-twisted Hamiltonian partition function, not an insertion of a possibly signed physical parity into an untwisted Gibbs trace. I/P/C are not three doubling axes.

The replay checks all nine file hashes against audit/independent/streamed_heat_audit.json and verifies beta, shift, length and seam labels. It consumes the full rational enclosures, rounds sector endpoints outward to a 10^-12 grid, and records every source hash. It does not rerun the original physical Horner computation. The independently audited real, self-adjoint Hilbert-Schmidt thermal history transfer, its A4 decomposition and its physical identification remain inherited analytic premises; see audit/APPENDIX_A_BRIDGE.md and heat_trace/PROOF.md.

For each even length k, write raw seam traces as Z_k,P_k,C_k. The sector moments are

    I_k=(Z_k+3P_k+8C_k)/12,
    O_k=(Z_k+3P_k-4C_k)/12,
    N_k=(Z_k-P_k)/4,
    Z_k=I_k+2O_k+3N_k.

Each sector is an actual eigenvalue list on the irreducible multiplicity space. O is one member of a conjugate pair; N is one copy of the three-dimensional representation's multiplicity space. Eigenvalues within these lists are counted with their ordinary positive integer spectral multiplicities. One occurrence of lambda contributes exactly lambda^k, not an arbitrary adjustable weight. Identical eigenvalues may occur repeatedly; selecting one occurrence still allows subtraction with coefficient one. The factors 1,2,3 are reinstated in the physical trace. They must not be used twice.

No finite dimension/count for the thermal transfer's nonzero spectrum is assumed. It may be infinite; compactness and trace-class even powers suffice. In particular its atom count is not 3^L or the MPS bond dimension. The physical Hilbert-space dimension is only used in the original finite trace computation, not as a thermal-transfer rank.

There are no independently computed beta=21 inputs among these nine files. The statement about missing inputs refers to this beta=10.5 moment package; it does not invent a second-temperature interpretation of a seam label.

## Tail Hankel argument with correct interval directions

Set x_i=lambda_i^2>=0. The length6/8/10 data give m3=sum x_i^3, m4=sum x_i^4, m5=sum x_i^5 in each sector. If x is any one atom, the remaining spectrum has moments rj=mj-x^j>=0. Cauchy-Schwarz gives r3*r5>=r4^2.

Let a be the upper endpoint of m3, b the lower endpoint of m4 and c the upper endpoint of m5. For every feasible x,

    (a-x^3)(c-x^5) >= max(0,b-x^4)^2.

The direction uses upper residuals on the product and the nonnegative lower residual on the squared term. Squaring a negative lower endpoint would be invalid. The replay explicitly proves c^4<b^5, so x^5<=c ensures x^4<b throughout the entire feasible domain. Thus its necessary condition is the polynomial inequality

    F(x)=a*c-b^2-c*x^3+2*b*x^4-a*x^5 >=0.

For each listed rational x_cap the code proves F(x_cap)<0, x_cap>=4b/(5a), and -3c+8b*x_cap-5a*x_cap^2<0. Since F'(x)=x^2[-3c+8bx-5ax^2], that derivative is negative thereafter: the bracket is decreasing for x>=4b/(5a). Hence all x>=x_cap are excluded. Positive residual constraints are respected, and any violation already excludes the atom. The square root of x_cap is enclosed by exact integer bisection for display.

This test is necessary for a residual spectrum, not sufficient for realization by an integer-counted spectrum. We use it only to prove an upper support cap, where necessity is enough. A passing test would not prove a transfer exists, identify its actual leading atom, or certify a thermal seed. No unseen count/flat-extension sufficiency assumption is used.

Mathematically this is an optimized family of square-filter bounds. A two-by-two positive residual Hankel matrix says the residual sum of x_i^3(u+v*x_i)^2 is nonnegative for every u,v. It refines, rather than replaces or discovers, the original proof's explicit square filters lambda^6(-2+10lambda^2)^2 and lambda^6(-25+100lambda^2)^2. Improvements in the trivial/vector caps are small, as expected from their already effective filters.

## Certified longer traces

Put h=x_cap^5 and let M be the sector's upper fifth moment. Every y_i=x_i^5 lies in [0,h] and sum y_i<=M. For any real r>=1, convex packing gives

    sum y_i^r <= q*h^r+(M-q*h)^r,  q=floor(M/h).

For even length L>=10 take r=L/10. The replay evaluates this as q*x_cap^(L/2)+(M-q*h)^((L/2)/5), using an exact rational upper fifth root. Therefore L need not be divisible by10; lengths24 and48 are valid. This is the original convex mass-packing step, extended to nonintegral exponents with directed roots, not a new full-spectrum calculation. The total adds sectors with multiplicities1,2,3. results.json records bounds at every even L from10 through120.

Using an upper support endpoint in this packing is safe even if no actual atom reaches it. It relaxes the feasible set. If repeated leading eigenvalues exist, they are included by q and the residual mass; no uniqueness is presumed.

## Cooling-only seed test

For a normalized archived D26 trial at numerator length2n with shifted total Rayleigh quotient R, Jensen gives Lnum=exp(-2 beta R)<=Z_(2n)(2 beta). With U>=Z_n(beta), Gibbs positivity gives Z_n(2 beta)<=Z_n(beta)^2<=U^2. Hence the fixed certified recipe can use

    J=Lnum/U^4,  C=J,
    a1=G(J),  b1=G(J^2*a1),
    G(z)=1-(1-z)^2/(2z^2).

The identification and staircase basepoints are those independently checked in nonperturbative_mps_review/REVIEW.md: a1 bounds P_t(2n,2 beta), and b1 bounds P_x(2n,4 beta). A nonpositive preceding output cannot be inserted into another update. This use of C=J genuinely avoids separately calculated2beta inputs.

All available exact archived numerator lengths relevant here were tested:20,24,28,32,40,48,72,120, at beta=21/2 and denominator n=10,12,14,16,20,24,36,60. The ground-length file's physical manifest hash is checked; the old72/120 contraction is the file already audited in APPENDIX_A_BRIDGE.md and is separately hashed here. Exact shifted Rayleigh quotients and rigorous exponential intervals are recorded.

The computed J values are approximately .04258,.07295,.11643,.17157,.30110,.42558,.61292,.55774, respectively. The first five fail the first G; the last three fail the second G. The replay checks the upper end of numerical evaluation as well, so failure is not merely roundoff in a lower approximation. These failures concern this specified upper-envelope recipe at this beta. They do not prove the exact physical ratios fail, nor an all-beta exclusion, nor an obstruction to all MPS methods.

At n24 the first G is strictly below2/5, and G(2/5)<0. Since C<=1, even an ideal C=1 would leave the second G negative with this fixed J. Thus tighter2beta upper traces alone cannot rescue n24 while retaining this denominator envelope, numerator and two-G initialization. The existing necessary screens' unresolved beta window [539/64,339/32] includes10.5 but is not evidence of feasibility; this new test supplies an actual certified input bound and finds it too weak at that point.

## Comparison with the successful old route and missing work

The original route already avoids direct2beta heat calculations by stronger use of ground-plus-tail information. It uses the N120 negative shifted trial energy, long-length transfer/sector bounds, cooling from21/2 to105/4, dominance forced by Z120>1, sector multiplicities, and a ground-relative thermal tail bound. Its final seeds compare lengths60/120; its audited all-integer gap result begins at L1920. Bare cooling U(2beta)<=U(beta)^2 discards precisely the mass structure that made that route work. Its success must not be claimed as a new discovery from the present failed cooling-only scan.

A smaller seed would need sharper upper traces at the initial beta, a better/richer numerator, an improved initialization, or a new ground/sector-tail construction. The archived upper moments only cover beta10.5. Other beta transfers are different operators; powers of X_(10.5) change spatial length, not beta. Physical Gibbs cooling yields valid coarse inequalities, but cannot be relabeled as independently computed moments of X_21.

If a route at n36 or another size benefits from sharper21 upper traces, one could separately certify the nine small physical heat inputs at beta21 and repeat this transfer analysis. This would be a new thermal-input campaign, not a new full-spectrum diagonalization. The current finite-input run metadata sum to about388 recorded compute seconds for all nine beta10.5 computations (length10 contributes about383 seconds); these are historical timings, not a guarantee on current hardware. Doubling beta requires rebuilding the exponential approximation, truncation/tail certificate and error budget, plus independent validation. A rough linear-in-polynomial-degree timing expectation is only a planning estimate. A short bounded beta21 L6 pilot is the appropriate next cost gate before scheduling L10. No such pilot was launched.

Direct heat-trace computation at length24/48 is unnecessary for the present bounds and would be exponentially more expensive. Conversely, adding a new D26 Rayleigh contraction would supply only a numerator; it would not automatically close the present upper-trace bottleneck. No new96 or other large-length contraction was launched just to populate an already weak cooling-only scan.

## Reproduction and limits

Run python replay.py from any working directory. It enforces CPU affinity, one GiB address space and180 CPU seconds; actual work is about one second. No eigensolver is imported. Results are a producer artifact awaiting independent review. Root files, original data, prior seals and GitHub were not modified. INPUT_SHA256.json identifies consumed inputs; MANIFEST_SHA256.json seals this new folder's replay and report.
