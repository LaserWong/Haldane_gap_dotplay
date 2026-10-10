# Independent review: moment-envelope optimality and unit-count witnesses

2026-10-10 18:54 EDT / 22:54 UTC. Independent scoped PASS.

## Verdict

The frozen package's principal mathematical claims pass independent exact arithmetic and analytic review:

1. The Hermite/Radau envelope is exactly optimal for the stated fixed-moment positive-measure relaxation on the closed support interval.
2. Separate explicit integer-multiplicity spectra satisfy every one of the nine original raw I/P/C intervals simultaneously, the certified support caps, A4 copy multiplicities, and positive I/P/C traces at every integer length L>=2.
3. Those unit-count spectra bound the possible improvement of the reported moment-only upper envelope by less than7.1643e-5 atL26 and3.0482e-5 atL100.
4. Integer counting nevertheless allows a genuine strict improvement: the trivial-sector L26 Hermite bound can be decreased uniformly by a rational delta>1.49e-14.

None of these claims constructs a Heisenberg thermal transfer or a beta-dependent physical family. No n50/n48 obstruction, minimum seed, new gap, or lower error bar on the actual physical trace follows. The auxiliary MPS96/100 contractions are excluded from this acceptance and require separate review before scientific use as new anchors.

Producer manifest SHA-256: `c862245e77fdf20e4e85859cbca804d888c96c11efcab2c30b5cbfedca3906cd`. All18 entries match. The original moment assessment, its independent review, and the n52 Hermite review seals also pass. No producer/root/GitHub files or previous seals were changed.

## 1. Three distinct optimization domains

For one sector, let x=lambda^2 and0<=x<=h. The inherited moments m3,m4,m5 are length6,8,10 transfer moments at beta0=21/2, with the extensive shift a=700741/500000. The source I/P/C labels are physical seam rotations0,pi,2pi/3. The full trace reconstructs as I+2O+3N from one trivial, one complex multiplicity list, and one vector multiplicity list. The latter lists have2 and3 identical physical copies.

An actual multiplicity-space spectrum gives the measure

    nu = sum_i x_i^3 delta_(x_i),
    integral1 dnu=m3, integralx dnu=m4, integralx^2 dnu=m5.

The relaxed optimization permits arbitrary positive masses in nu. A mass at positive x has effective spectral multiplicity mass/x^3, which need not be an integer. This relaxation is not the class of ordinary eigenvalue lists. Allowing a formal mass at0 is also a relaxation; zero eigenvalues themselves contribute no x^3 mass. The explicit relaxed maximizers here use strictly positive support nodes, so that distinction causes no hidden atom at0 in the construction.

The stricter abstract class requires literal integer multiplicities in A4 multiplicity spaces, all nine raw interval constraints, support caps, and positive A4 seam traces at every integer L>=2. The constructed witnesses belong to that class. They are finite-rank positive diagonal operators, not a physical Hamiltonian family. No bound on thermal-transfer rank follows from the nine inputs.

The physical Heisenberg class additionally requires the specified Hamiltonians, physical dimension3^L, compatible traces at other temperatures, and the actual thermal-history construction. Neither witness class is asserted to meet those requirements. In particular, single-beta trace feasibility is not cross-temperature Gibbs realizability.

## 2. Exact relaxed primal-dual equality

Fix the exact rational midpoint triple a,b,c of one sector's outward intervals. Define

    t=(h b-c)/(h a-b),
    wh=(b-t a)/(h-t), wt=a-wh.

The checker independently verifies0<t<h, positive masses, and

    wh+wt=a,
    wh h+wt t=b,
    wh h^2+wt t^2=c.

Thus nu=wh delta_h+wt delta_t is feasible for the fixed-moment relaxation. The closed support[0,h] is the optimization domain here; the proof does not assert that an endpoint atom at the conservative cap is attained by the actual thermal transfer. Every explicit integer witness lies strictly below the cap.

For even L>=10 put k=L/2-3>=2. Let Q(x)=a0+b0 x+c0 x^2 interpolate x^k at t,h and its derivative at t. The n52 review already proves the global identity

    Q(x)-x^k=(h-x)(x-t)^2 P_(k-3)(x),

where P has positive coefficients for k>=3; for k2 the difference vanishes identically. Here those coefficients are independently reconstructed as

    coefficient of x^j = sum_(a=0)^(k-3-j) (a+1)t^a h^(k-3-j-a).

Full coefficient identities are checked independently at the representative degrees needed forL26 andL100, and the exact three interpolation equations and center equality are checked for every even L10..120. The general positive-coefficient formula supplies the proof for all k, rather than relying on a numerical sampling grid.

Therefore Q>=x^k on the entire closed support, including0. Every feasible positive measure satisfies integralx^k dnu<=integralQ dnu. The two-node measure attains equality because Q=x^k at both its support nodes. This proves exact primal-dual equality for each fixed-moment problem, simultaneously for all even L>=10.

The effective spectral counts wh/h^3 and wt/t^3 are rational nonintegers in every sector. The checker verifies both nonintegrality statements exactly. Their approximate values are(0.999999973389,53.0287405863),(0.999999081069,85.0585119113),(0.999999926566,109.441094623). Rounding these counts is not a moment-preserving operation and is explicitly rejected in the adversarial tests.

The relaxed optimizer is not promoted to an integer spectrum. Nor does the fact that one optimizer is noninteger alone prove a positive integer-optimality gap; the separate strict correction below supplies that argument.

## 3. Correlated raw intervals and signed endpoints

The independent checker rereads all nine original physical certificates, validates their trusted streamed-audit hashes, beta, shift, seam angle, and length, and reconstructs the outward sector intervals using coefficient-aware rational arithmetic.

For each candidate sector triple, it recombines

    raw_I=I+2O+3N,
    raw_P=I+2O-N,
    raw_C=I-O.

Both the central relaxed witnesses and the separate integer witnesses lie strictly within all nine raw intervals. All18 exact comparisons pass, and every nearest-endpoint margin exceeds1.95e-11. Thus compatibility is not inferred merely from independently chosen sector boxes. The adversarial check demonstrates that choosing all three sector upper endpoints violates the original raw identity interval at each of6,8,10; cross-sector correlations are real and cannot be ignored.

For an uncertain moment triple, the polynomial combination uses upper endpoints for positive coefficients and lower endpoints for negative coefficients. This bounds every feasible sector box and therefore the narrower correlated raw set. A feasible central relaxed witness bounds that interval-relaxed optimum from below. It does not prove that the entire interval optimum equals the central value.

AtL26, the interval-relaxed optimum is bracketed within3.79023e-8; atL100 within3.36822e-8. These are bounds on the stated information problem. The relaxed central measure is not claimed to satisfy all-integer seam positivity.

The independent report includes outward rounding of the reported upper endpoint itself when forming improvement gaps. The producer's gap quantities are computed against the exact unrounded polynomial envelope before a10^-30 reporting grid. Adding the final upper rounding is harmless but makes the comparison with the displayed upper endpoint completely explicit. All quoted decimal targets remain valid.

## 4. Literal unit-count construction and compressed tiny block

The three base multiplicity-space lists contain counts(1,53,1),(1,85,1),(1,109,1), each at three exact rational squared eigenvalues. The checker reads those rational proposals and verifies them without importing the numerical proposal generator. The actual eigenvalues are the positive square roots. Every squared eigenvalue is strictly inside its inherited support cap.

The trivial list also contains exactly10^15 copies at x=10^-10, so lambda=10^-5. This is an integer count stored in compressed form, not a fractional spectral weight or a numerically truncated cluster. Its exact contributions at lengths2,3,6,8,10 are respectively

    10^5, 1, 10^-15, 10^-25, 10^-35.

Every term is included in the raw interval comparisons. Omitting the block makes C2 negative, as independently checked; including it repairs that constraint while preserving the small higher moments. Ignoring its small but nonzero higher-moment contributions would be invalid.

With the physical copy factors restored, the abstract rank is

    (10^15+55)+2*87+3*111 = 10^15+562.

No giant vector or matrix is allocated. A diagonal operator with these repeated positive eigenvalues and the appropriate A4 irreducible representation factors is a valid finite-dimensional self-adjoint, compact, Hilbert-Schmidt abstract operator. The enormous rank is not3^L, not26, and not a retained low-energy count. Neither a local Heisenberg Hamiltonian nor a relation between operators at different beta is constructed.

### Positivity at every integer length

All eigenvalues are positive, so all sector moments and raw_I are positive. The leading trivial x is greater than1, hence I_L>1. Every complex/vector x is less than1, so their moments decrease with integer L. Exact rational calculations give O6<1 and N8<1. Therefore

    raw_C=I_L-O_L>0 for every L>=6,
    raw_P=I_L+2O_L-N_L>0 for every L>=8.

The remaining lengths2..7 are checked individually. For odd L the checker encloses sqrt(x) on a separate10^-40 grid, then uses lower positive terms and upper negative terms. Every resulting P and C lower bound is strictly positive. These facts cover every integer L>=2 and all nonidentity A4 seam classes, including inverse3-cycles. They do not claim positivity for arbitrary untested SO(3) twists or a physically realizable cross-beta family.

## 5. What the quantitative envelope gaps prove

Let U_L be the current rigorous Hermite envelope and W_L the exact trace of the constructed integer spectrum. Any universally valid upper bound using only the defined abstract information must be at least W_L. Consequently its improvement below U_L cannot exceed U_L-W_L.

After accounting also for the outer reporting-grid rounding, the independent exact bounds are

- L26: improvement<0.000071642704909761, hence<7.1643e-5;
- L100: improvement<0.000030481133552225, hence<3.0482e-5.

All56 even lengths10..120 and the producer's relative-gap expressions pass independent verification. The same fixed witness supplies every length, rather than choosing unrelated spectra for different objectives.

These statements do not locate the true physical Heisenberg trace within the envelope. Additional Hamiltonian identities, other moments, or cross-temperature constraints may substantially reduce it. They also do not bound an optimized cooled-bootstrap seed recipe: that algorithm combines several moments, actual anchors, continuous cooling parameters, and recurrent updates. A global exclusion would require a separate precisely defined domain and rigorous enclosure argument. Neither a floating failure nor this near-optimality result proves n52 minimal or rules out n50/n48.

## 6. Independent proof of strict integer improvement

At trivial-sector L26 let Q majorize x^10 and set

    Delta=sum_i x_i^3[Q(x_i)-x_i^10].

The exact polynomial factorization gives Q-x^10=(x-t)^2(h-x)R(x), with every coefficient ofR nonnegative and its constant term at least h^7. Hence

    Delta>=h^7 sum_i x_i^3(x_i-t)^2(h-x).

The checker reconstructs this quotient from the explicit coefficient formula, without SymPy or producer polynomial division, and matches every recorded coefficient.

Take eps_t=eps_h=10^-5. If all x_i<=h-eps_h, then

    Delta>=eps_h h^7(m5-2t m4+t^2 m3)>=dH>0.

The last lower bound uses m5_lower,m4_upper,m3_lower. If Delta<dH, there must instead be at least one atom above h-eps_h. Its unit multiplicity consumes at least(h-eps_h)^3 of m3. The near-t interval is disjoint from this high interval, and each atom there consumes at least(t-eps_t)^3. Thus its integer atom count is at most

    floor([m3_upper-(h-eps_h)^3]/(t-eps_t)^3)=53.

This step is invalid for freely weighted measures and is precisely where integer multiplicity adds information.

Define g(x)=x^3(h-x)/(t^3(h-t)). Its sum has the lower bound

    sum_i g(x_i)>=(h m3_lower-m4_upper)/(t^3(h-t)).

On the near-t interval, g is increasing because its derivative has sign3h-4x and t+eps_t<3h/4. Each such atom contributes at most g(t+eps_t). Outside that interval, the polynomial slack inequality implies

    g(x)<=K x^3[Q(x)-x^10],
    K=1/[t^3(h-t)eps_t^2 h^7].

At x=0 orh both relevant sides vanish, so no division by a zero endpoint is required. Summing yields sumg<=53g(t+eps_t)+K Delta. The certified lower total exceeds the first term by a positive rational deficit. Combining the two cases proves

    Delta>=min(dH,deficit/K)=delta,
    delta≈1.498515849348223e-14>149/10^16.

This is uniform over all archived trivial-sector moment intervals, so it remains valid with raw cross-sector restrictions. Subtracting delta from the signed-endpoint Hermite upper is rigorous. It also proves that at the exact fixed central moments, any integer realization has a strict gap below relaxed equality, rather than inferring that conclusion solely from a noninteger optimizer.

The correction is deliberately small. It does not determine the best integer correction, and it does not resolve a smaller bootstrap seed.

## 7. Reproduction and limits

Run `python independent_check.py > replay.log` and `python adversarial.py > adversarial.log` in a disposable copy to preserve seals. The exact replay uses Python standard-library rational arithmetic, independent integer square-root bounds, direct raw-interval reconstruction, and explicit polynomial coefficients. It imports no producer module, numerical optimizer, eigensolver, or contraction engine. CPU5,700MiB/600CPU-second limits; observed replay cost about0.42CPU seconds and11.3MiB RSS.

Auxiliary MPS96/100 files are preserved and hash-checked as package contents only. Their contractions were not reproduced here and are not dependencies of any accepted claim in this review. All earlier gap certificates remain unchanged. INPUT_SHA256.json identifies consumed inputs; independent_results.json gives exact witnesses, margins, and corrected reporting gaps; CLAIM_VERDICTS.json and the manifests freeze the accepted scope.
