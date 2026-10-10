# Independent review: uniform transfer moment refinement

Updated 2026-10-10 18:19 EDT / 22:19 UTC.

## Verdict and scope

PASS for the new support caps, longer even-length upper traces, and bounded failure statements, conditional on the explicitly inherited physical heat certificates and self-adjoint thermal-history transfer identification. No substantive error was found in the producer package.

The independently validated outward bounds are

- |lambda_trivial| < 1.002405557347;
- |lambda_complex| < 0.701394814709;
- |lambda_vector| < 0.886398506317;
- Z24(21/2) <= 1.238492320537;
- Z48(21/2) <= 1.131484383792.

All eight reported fixed cooling-only starts fail. These are failures of the specified certified bound recipe, not of exact physical ratios, not an all-beta exclusion, and not a new theorem excluding smaller seeds or other MPS constructions. The n24 ideal-C obstruction has the same restricted meaning.

The assessed manifest hash is `80bd49ef30c697bd076cfa930c236e6b9f40931b47304e508891483da1f15739`. Its six entries and every producer input hash match. The independent checker neither imports nor runs producer code. It reconstructs moment intervals, locates caps with a different integer-grid search, uses integer comparisons for directed roots, and uses a different exponential enclosure. It verifies all 56 even-length bounds from 10 through 120, not only 24 and 48. No root, producer, archived physical-data, or GitHub files were changed. The shared snapshot has no Git metadata; branch/commit status is unavailable here.

## 1. Physical and representation-theoretic premises

The Hamiltonian is the uniform periodic spin-1 Heisenberg chain with bilinear bond coefficient one. All nine inputs use beta=21/2 and shift a=700741/500000, at lengths 6,8,10. Their physical Hilbert dimensions are 729,6561,59049. The I/P/C labels denote seam rotations by 0, pi, 2pi/3, as checked in every certificate, and do not label different temperatures or spatial/thermal doubling axes.

This review reads heat_trace/PROOF.md and audit/APPENDIX_A_BRIDGE.md. It inherits, rather than recomputes, their complete physical heat enclosures and exact identification with a real self-adjoint Hilbert-Schmidt transfer X_beta. The independent streamed audit's nine certificate hashes all match. Likewise, exact D26 contraction integers are inherited archived physical trial data; no new D26 tensor contraction is claimed here.

The A4 isotypic decomposition is the orthogonal direct sum of V_r tensor M_r. A commuting self-adjoint X acts as identity on V_r times a self-adjoint compact operator on M_r. Thus its eigenvalues in each multiplicity space have ordinary positive integer spectral multiplicities. The real structure identifies the two complex one-dimensional representations with equal spectral lists. The three character rows, after combining that conjugate pair, are

    Z = I + 2 O + 3 N,
    P = I + 2 O - N,
    C = I - O.

The inverse is

    I = (Z + 3P + 8C)/12,
    O = (Z + 3P - 4C)/12,
    N = (Z - P)/4.

The checker verifies the complete inverse matrix exactly. O counts one complex sector and N counts one vector multiplicity space. Physical reconstruction alone restores factors 1,2,3. A P input is a positive partition function of a seam-twisted physical Hamiltonian; it is not a signed physical parity expectation in the untwisted Gibbs state.

X can have negative eigenvalues. We use only even lengths, put x=lambda^2, and identify length 6/8/10 with moments sum x^3, sum x^4, sum x^5. Length L then uses x^(L/2), never x^L or lambda^(L/2). No statement about odd-length positivity is needed. Neither physical dimension 3^L nor MPS bond dimension 26 bounds thermal-transfer rank.

## 2. Infinite-rank residual positivity and interval direction

For one occurrence x of an eigenvalue square, remove just that occurrence. The remaining countable spectrum has nonnegative moments r_j=m_j-x^j. Finite m3 and m5 put the sequences of residual x_i^(3/2) and x_i^(5/2) in l2, so Cauchy-Schwarz gives r4^2 <= r3 r5, also for infinitely many eigenvalues. Repetition of an eigenvalue poses no problem: one copy is removed and other copies remain. An arbitrary weighted measure would not justify subtraction with coefficient one; integer spectral multiplicity is essential.

Let a=m3_upper, b=m4_lower, c=m5_upper. If x is feasible, then 0<=r3<=a-x^3, 0<=r5<=c-x^5 and r4>=max(0,b-x^4). Hence

    (a-x^3)(c-x^5) >= max(0,b-x^4)^2.

Both product factors must be upper residual bounds, and the lower squared bound must be clamped at zero. The code checks interval-coefficient signs and rounds outward to a 10^-12 grid, exactly matching the producer's moment boxes. For all three sectors, b>0 and c^4<b^5. On the feasible domain x>=0, x^5<=c, so x^4<=c^(4/5)<b. Therefore the clamp is inactive throughout that whole feasible domain, not just near the reported cap. The necessary polynomial condition is

    F(x)=ac-b^2-c x^3+2b x^4-a x^5 >=0.

This is a necessary condition only. Passing it would not prove that a spectrum with integral atom counts exists.

## 3. Global exclusion, not merely numerical root finding

The independently found rational caps for x are

- trivial: 5024084507/5000000000;
- complex: 4919546861/10000000000;
- vector: 98212789/125000000.

For each cap d, exact rational arithmetic proves F(d)<0, d>=4b/(5a), and Q(d)<0 where Q(x)=-3c+8b x-5a x^2. Since Q'(x)=8b-10a x<=0 for all x>=d, Q remains negative there; F'(x)=x^2 Q(x)<0 there. Thus F(x)<0 for every x>=d. Any such x either already violates residual nonnegativity or violates the necessary determinant condition. Every possible larger root or disconnected feasible interval is excluded. Merely printing a polynomial root or F(d)<0 would not suffice; these derivative checks provide the missing global-domain argument.

The exact margins are in independent_results.json. Squared-root upper displays are checked by raising a rational upper root to its integer power. Compactness ensures a nonzero maximal modulus, although the longer trace bound needs only the weak cap x<=d.

## 4. Directed longer-length trace packing

Let y_i=x_i^5, h=d^5, and M=m5_upper. Then 0<=y_i<=h and sum y_i<=M. For any r>=1, shifting mass from a smaller non-full atom into a larger one cannot decrease sum y_i^r. The finite-list maximum is q h^r+(M-qh)^r, where q=floor(M/h). The bound is nondecreasing in available mass, so it applies to a partial finite sum even if its total is smaller than M. Taking monotone limits establishes the same result for infinitely many atoms. No finite rank or leading-eigenvalue uniqueness is assumed.

For even L>=10, r=L/10. The evaluated upper bound is

    q d^(L/2) + ((M-q d^5)^(L/2))^(1/5).

The fifth root is bounded upwards by exact integer comparisons. Fractional exponents at lengths 24 and 48 are therefore rigorous. The independently computed 10^-36 root-grid bounds are no larger than the producer's 10^-24 root-grid and 10^-30 outer-rounded bounds. Every sector bound, q value, and total weighted by 1,2,3 passes. The final 12-decimal figures quoted above are outward, not nearest-rounding claims.

## 5. Cooling-only recipe and the n24 limitation

For a normalized length-2n trial with shifted total Rayleigh quotient R, Jensen gives exp(-2 beta R)<=Z_2n(2 beta). The archived H0/N0 outputs are total energies; the older U_L/V_L outputs are per-bond energies and must be multiplied by L. The checker independently handles that distinction and adds a L once.

Given U>=Z_n(beta), positive Boltzmann weights imply Z_n(2 beta)<=U^2, even if some shifted energies are negative. Therefore the reported certified lower-input recipe sets J=C=exp(-2 beta R)/U^4. The independently reviewed staircase gives first G(J), then G(J^2 G(J)), with G(z)=1-(1-z)^2/(2z^2). G is increasing on 0<z<=1. A nonpositive first output cannot be inserted as a subsequent valid lower input.

The checker encloses each exponential with a different 64-term positive Taylor expansion at argument at most 1/8, a rigorous geometric remainder, repeated directed squaring, and reciprocal bounds for negative arguments. Its resulting J interval lies inside the producer's interval in every case. It verifies the stated G values algebraically and proves failure using the upper endpoint, excluding numerical rounding as the explanation.

| Denominator n | Approximate J | Failed update |
|---|---:|---|
| 10 | 0.042577204234 | first G |
| 12 | 0.072954918198 | first G |
| 14 | 0.116428107539 | first G |
| 16 | 0.171572295389 | first G |
| 20 | 0.301103964159 | first G |
| 24 | 0.425577399248 | second G |
| 36 | 0.612921440582 | second G |
| 60 | 0.557737221344 | second G |

At n24 the first output is approximately 0.0890890351381, rigorously less than 2/5. Even replacing C by its largest possible value 1 leaves the second argument <=G(J)<2/5, and G(2/5)=-1/8<0. This rules out rescuing that two-G initialization by improving only the 2beta denominator while retaining the initial beta envelope and fixed numerator. It does not rule out sharpening the beta envelope, changing the numerator, another update order, another beta, or ground/sector-tail information. The physical J itself has not been upper-bounded by this calculation.

## 6. Novelty relative to the successful archived route

The residual Hankel condition is an optimized two-coefficient square-filter necessary condition: for every u,v, the residual sum x_i^3(u+v x_i)^2 is nonnegative. It refines the archived filters lambda^6(-2+10lambda^2)^2 and lambda^6(-25+100lambda^2)^2; it does not discover positivity filters. The checker revalidates those fixed filters and their monotonicity beyond the old caps against the current intervals.

Applying the archived old caps and old tenth-moment constants to these even lengths by the same directed fractional-power extension gives

| Inputs/caps | Z24 upper | Z48 upper |
|---|---:|---:|
| Old caps and old moment constants | 1.240171225699 | 1.133890906770 |
| Old caps, current tight fifth moments | 1.240167384191 | 1.133890879574 |
| New Hankel caps and current moments | 1.238492320537 | 1.131484383792 |

These first two rows are this review's evaluations of the old formulas at 24/48, not a claim those lengths were printed in the original proof. This separates tighter archived moment arithmetic from the cap refinement. The gain is genuine but small. The original mass-packing argument already applies to real exponents r>=1; the new implementation supplies explicit directed roots at the requested lengths.

The successful old route uses the negative shifted N120 trial energy, sector multiplicities, cooling to beta=105/4, forced dominant transfer weight, and a ground-relative thermal tail. Its seeds compare 60/120, with the separately audited gap statement beginning at all integer L>=1920. Bare cooling loses structure needed there. The present failed scan neither invalidates nor newly reproduces that full gap theorem. Powers of X_(21/2) vary spatial length, not beta; no independent beta=21 input campaign occurred.

## 7. Reproduction, adversarial tests, and remaining work

Run `python independent_check.py` in this directory. It writes only this review's JSON and runs on CPU5 when allowed, under a 1 GiB virtual-memory and 180 CPU-second ceiling. Observed runtime is about 1.5 CPU seconds and 11 MiB resident memory. It uses the Python standard library only; no eigensolver or many-body spectral construction is used.

The tests include signed/repeated eigenvalues, an exact infinite geometric unit-atom spectrum, the failure of arbitrary weighted-atom subtraction, a negative-lower-residual counterexample to unguarded squaring, a counterexample to using a lower m3 product endpoint, all corners of character interval boxes, 625 finite packing examples, and directed roots at zero and above one. These tests supplement the proofs above; they are not substitutes for them.

No new scientific computation is required to accept this bounded package. Improving a seed remains open. A sharper beta=21 denominator may help another size but cannot rescue n24 under the fixed envelope/numerator/two-G recipe. A new beta=21 physical heat campaign, a richer numerator, or a different ground/sector-tail initialization would need separate certification and authorization; none was launched here.
