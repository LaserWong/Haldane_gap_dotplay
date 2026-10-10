# Independent continuous ordinary-bilayer review through g = .09

Updated 2026-10-10 17:25 America/New_York (EDT) / 21:25 UTC.

## Accepted theorem and scope

For the ordinary periodic square spin-1/2 bilayer, unit rung exchange, two straight intralayer exchanges g, no crossed exchange, and positive-direction periodic bond multiplicity retained, every real g in [17/200,9/100] and every integer square side L >= 2 has a unique finite-volume ground state and

    gap(H_L(g)) >= 2894183477/500000000000 = .005788366954.

The seven adjoining closed pieces are certified individually. Joining the independently sealed 49-piece [0,17/200] theorem yields 56 closed pieces covering every real g in [0,9/100], with

    gap(H_L(g)) >= 486442811/250000000000 = .001945771244.

These are sufficient rigorous lower bounds, not estimates of the physical gap or critical coupling. No physical-gap monotonicity, interpolation of discrete gap results, arbitrary aspect ratio, or infinite-volume uniqueness is asserted. This is analytic reasoning with independently replayed exact arithmetic, not a formal proof-assistant result.

## Provenance and independence

The producer freeze is 8a135f1a729f5f00953b96b3b9ed61891653ca3d592e27d492d29031d1652698. Its 23 files are copied byte-for-byte under snapshot. Before importing any mathematical helper, the audit verifies this freeze, every snapshot file, 107 direct inputs, and all 14 inherited seals. In particular:

- Prior continuous review: c14cdb65f0e1b92a6025758e63352e404eef01965f7dde2344a2eaaf86c5a0b9
- Exact physical third-moment review: 7d85c62626ca0aee9fa90fd5ca9968dac5ce50c34c4d023bf916df593cdfee36

The latter independently reconstructed every geometry entry and accepted the fixed enlarged physical space; its discrete .09 result is not used as an interval-gap premise. Its .10 matrix agreement here likewise establishes no .10 gap theorem.

No producer mathematical module is imported or executed. The denominator polynomial, directed arithmetic and scalar logic are reused from the sealed independent interval reviews. The new fixed-basis numerator is reconstructed by the sealed independent physical matrix assembler. The copied scalar_record function is AST-compared against the old independent audit, allowing exactly two substitutions: the coupling domain and replacement of the old filtered numerator by this fixed 43-dimensional Rayleigh numerator. Every other scalar, trace, finite-window and short-size check is identical. The module-boundary guard rejects imports outside the four inherited review directories and this review. No eigensolver runs.

## Fixed physical numerator over the whole interval

Write H'(g)=H(g)+3N/4=Q+(g/2)A, with N=64. Let B contain the vacuum and fourteen two-triplet spin-singlet pair-orbit vectors. Put L=A42 B_pair, R=A44 L, M=A64 L and U=R+M. These are coupling-independent physical vectors; L,R occupy q=4, M occupies q=6. The fixed family is (B,L,U), with 43 columns.

The independently reconstructed contractions F=L*L, S=L*R, V=R*R, W=M*M, X=R*A44 R, Y=R*A46 M, Z=M*A66 M give

    G = [[D,0,0], [0,F,S], [0,S*,V+W]],
    A0 = [[D diag(0,2,...,2),0,0], [0,4F,4S], [0,4S*,4V+6W]].

D is diag(1,3 times each pair-orbit size). Direct graph action supplies the remaining interaction blocks: the B/L and B/U blocks are g EF/2 and g ES/2; L/L is 4F+g S/2; L/U is 4S+g(V+W)/2; U/U is 4V+6W+g(X+Y+Y*+Z)/2. The B/B interaction is independently assembled from the weighted periodic graph. Thus A(g)=A0+g A1 by an operator identity. Formal evaluations at 0 and 1 recover these coefficients without applying any gap theorem there. All positive rational Gram pivots are checked, giving exact rank 43. The full exported Gram and coefficient matrices agree, as do the complete separately saved .09 and .10 matrices.

For each interval the saved integer coefficient vector c is fixed. We verify its length, positive norm c*Gc, and both coefficients of

    rho64(g) = c*(A0+g A1)c / (c*Gc).

This is exactly affine for every real g in the interval. Endpoint and center evaluations are supplementary checks, not a replacement for affinity. Convexity of the exponential gives the physical trace lower bound Z64'(beta,g) >= exp(-beta rho64(g)), retaining exactly one normalized trial contribution. Neither a full residual, a new H^6 moment, nor q=8 support is used. Such data would be required for a new spectral denominator bound, which is not claimed. Search dimension 43 is distinct from the retained count 1 and physical Hilbert dimension 2^128.

## Unchanged smaller denominators

The N=16 and N=32 ground searches have dimensions 11 and 29. Their existing fixed bases have complete H'^2 matrices, including all leakage. Fresh exact reconstruction verifies the matrix polynomials; each fixed integer witness has positive norm, affine Rayleigh rho and complete convex quadratic variance v. For the oscillator reference

    r_q(g) = C(2g-1)+(C+q)sqrt(1-4g), C=3N/8,

r_q-rho is concave, so its endpoint minimum bounds the entire interval. Exact downward square-root enclosures preserve this direction. The positive q=1 margin identifies the unique even ground, and the q=2 margin with the endpoint variance maximum gives its uniform Temple width.

The unchanged odd family w_r(z)=e_r-z P3 V e_r/2 is held at the interval midpoint z. Its q=1 and q=3 pieces give exact bivariate moment reconstruction in physical coupling g. All N Fourier Gram symbols are positive, and each mode's first moment is affine and complete variance convex quadratic. The audit independently reconstructs the physical normalization, all seven-source polynomial coefficients, Q(sqrt(2)) Fourier symbols, 160-bit directed endpoint enclosures, positive Temple denominators and lower endpoints. The q=5 image contribution is retained. All 336 mode certificates and their within-interval diagnostic points pass.

The ground plus the 3N odd levels exhaust exactly the 1+3N levels below r_2 by the previously proved oscillator counting comparison and min-max principle. The retained counts are 49 and 97, not the total available search dimensions 59 and 125. Every omitted physical eigenvalue is covered by the positive bosonic tail with multiplicity binom(3N+q-1,q), q=2,...,N. These are reference oscillator multiplicities, not hard-core shell counts; excess positive terms are safe. Directed exponentials check every ground, odd-band and tail trace term.

## Correlated energy bounds and all integer sizes

The audit forms 8 rho16-2 rho64, 16 rho16-4 rho64, and 4 rho32-2 rho64 before taking the common coupling endpoint minima. The extensive shifts cancel exactly. No independent extremization destroys the affine correlation. Trace uppers and the single numerator lower yield the three initial ratios with downward rounding.

Every temperature-first and canonical state, component, sequential update argument, route merger, joint product, spatial base and inverse temperature is replayed. The formal partition-function exponent ledger checks that both orderings telescope to the same base identity. A previous base's joint bound is never propagated without rederivation.

All 41 finite dyadic windows are checked, including 34 required pre-asymptotic windows. They begin at L=8 and cover every integer through the next doubled side, not merely powers of two. Each terminal state meets u<=1/500 and its exact exponential small-defect witness; the largest onset is L=512. Seven final windows overlap their analytic tails and are checked even though unnecessary for coverage. The reported bound is the minimum of all required windows, the analytic tail, and every short-size bound.

For L=2,...,7 the vacuum has shifted Rayleigh zero. The explicit q=1 reference, with C=3 sum(edge multiplicity squared)/16, at the high coupling endpoint bounds the second eigenvalue; its derivative is nonpositive on this range. The periodic graph is rebuilt: the squared-edge-multiplicity sum is 16 for L=2 and 2L^2 otherwise. All 42 short-size rows pass. This uses monotonicity of an explicit comparison formula only. For long sizes the checked thermal purity exceeds one half, forcing a single ground state; the strict exponential witness then bounds its gap. For short sizes the positive second-level reference versus the vacuum identifies a unique ground directly.

## Coverage, replay and tests

The exact adjoining intervals and their all-size bounds are:

- [17/200,43/500]: .024024513414
- [43/500,87/1000]: .014301717985
- [87/1000,11/125]: .005788366954
- [11/125,177/2000]: .020470914121
- [177/2000,89/1000]: .014672573603
- [89/1000,179/2000]: .012353003785
- [179/2000,9/100]: .006892292777

Only after verifying all seven certificates, exact endpoint adjacency, and the unchanged earlier accepted interval do we take the minimum for [0,.09]. Deliberate corruptions target normalization, numerator coefficients/counts/support, denominator physical moments, directed odd endpoints, omitted tails, correlated energies, wrong-base products, finite windows, bootstrap, short multiedges, and coverage. Results are in results/adversarial_rejections.json. REPRODUCE.sh first verifies the immutable manifest, then runs fresh exact checks into a separate unsealed output directory. Each process is pinned to one CPU with BLAS thread count one and a 1 GiB address-space cap. Writes are confined to this review. The extracted workspace has no Git metadata; no remote publication or commit is claimed.
