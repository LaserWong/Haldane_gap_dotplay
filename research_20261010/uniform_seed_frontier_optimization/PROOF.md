# Uniform spin-one seed n52 by a Hermite moment majorant

2026-10-10 18:32 EDT / 22:32 UTC. Exact producer candidate; independent review pending.

## Result and scope

The existing nine beta0=21/2 physical seam inputs and the already independently accepted exact D26 MPS104 contraction suffice for the producer candidate

    gap(H_L) >= 19/5000 = 0.0038, every integer periodic L>=52,

with a unique ground state throughout that range. The canonical physical seed is n=52 at beta=567/25=22.68, base transfer moment length ell=26, and cooling ratio r=54/25. The small-defect regime begins at L=3328; every earlier integer window is separately certified. No result belowL52, no minimal seed theorem and no all-method obstruction is claimed.

This candidate improves the upper-moment calculation rather than adding physical thermal data, a new MPS contraction, or a full-spectrum calculation. Its new ingredient is a quadratic Hermite majorant over the already certified transfer support. Its second, quantitatively small refinement uses the actual negative MPS104 Rayleigh magnitude instead of retaining only its sign. Previously accepted n54/56/60 certificates and all seals remain unchanged.

## Dependencies and model

H_L is the uniform periodic spin-one Heisenberg chain, bilinear coefficient one. Use shifted traces Z_L(beta)=Tr exp[-beta(H_L+aL)], a=700741/500000. The nine inputs are physical length6/8/10 traces at beta0=21/2 with seam angles0,pi,2pi/3. They are not three temperatures or three geometric directions.

The exact self-adjoint Hilbert-Schmidt history transfer and its all-integer physical trace identity, A4 sectors, and multiplicities are the independently accepted inherited premises described in uniform_transfer_moment_assessment and uniform_cooled_seed_review. Write x_i=lambda_i^2>=0 in one multiplicity-space eigenvalue list. The sealed cap is0<=x_i<=h. The sector moments m3,m4,m5 are the length6,8,10 sums of x_i^3,x_i^4,x_i^5. Every spectral occurrence has unit weight; the full physical trace adds sectors I+2O+3N. Neither a finite thermal-transfer rank nor a finite atom count is assumed.

certify.py checks the frozen moment-result hash and reuses its exact outward sector intervals and support caps. It checks the accepted cooled producer's source hashes for the MPS104 integer output and related contraction files; the independently reviewed physical construction and fresh sequential reproduction of MPS104 are inherited from uniform_cooled_seed_review. No new contraction is run here.

## Quadratic Hermite majorant, including x=0

Let L>=10 be even, k=L/2-3>=2, and f(x)=x^k on[0,h]. Choose any rational interior node0<t<h. Define

    c = [h^k-t^k-k*t^(k-1)*(h-t)]/(h-t)^2,
    b = k*t^(k-1)-2*c*t,
    a0 = t^k-k*t^k+c*t^2,
    Q(x)=a0+b*x+c*x^2.

This polynomial satisfies Q(t)=f(t), Q'(t)=f'(t), and Q(h)=f(h). For k=2 it is exactly f. For integer k>=3, f'''(x)=k(k-1)(k-2)x^(k-3)>=0 throughout[0,h]. The Hermite interpolation remainder is

    f(x)-Q(x) = f'''(xi)/6 * (x-t)^2*(x-h) <=0,

with the usual limiting interpretation at repeated/end nodes. Hence Q(x)>=x^k on the whole closed interval, including x=0. An alternative direct proof for a polynomial follows by repeated Rolle's theorem; no analyticity outside[0,h] or strictly positive lower support is needed.

Multiplying by x^3>=0 gives x^(L/2)<=a0*x^3+b*x^4+c*x^5. At x=0 both sides vanish; we never divide by x or assign an artificial atom mass at zero. Sum over the compact transfer spectrum:

    sector_L <= a0*m3+b*m4+c*m5.

The sums converge because m3,m4,m5 are finite. Although b can be negative, this is a pointwise polynomial majorant with a nonnegative resulting sum. The code uses the upper moment endpoint for every nonnegative coefficient and the lower endpoint for every negative coefficient. This signed selection is essential. All coefficients, support endpoints, nodes and final bounds are exact rationals.

Node choice affects efficiency, not validity. The code takes midpoint moments M3,M4,M5 and forms

    t_raw=(h*M4-M5)/(h*M3-M4),

then rounds downward to the10^-10 grid and explicitly verifies0<t<h. The two-node Gauss-Radau expression motivates this choice; no quadrature existence, integer atom realization or optimizer sufficiency is assumed. Any accepted interior node proves the same kind of upper bound. The code takes the minimum of this Hermite bound and the previously accepted convex-packing bound.

The Hermite majorant is a different use of the same low moments. Packing permits its leftover fifth-moment mass to concentrate in a way incompatible with the third/fourth moments, whereas this polynomial retains all three simultaneously. This is why a seemingly small improvement at base26 changes startup feasibility. Floating displays show Z26(beta0) upper reduced from about1.203138386856 to1.1951235. Exact sector bounds and polynomial coefficients at the two needed lengths26/104 are in certificates.json.

## Cooled-sector construction and actual anchor magnitude

Use the already accepted direct-sector-power lemma in uniform_cooled_seed_optimization/PROOF.md and its independent review. Its parameters are now n=52,ell=26,r=54/25, so q=n/ell=2 and p=2n/ell=4. The generalized fractional-sector exponents of the earlier n54 result are not needed for this seed; the rational cooling ratio still uses directed roots.

Let A,B,C be the Hermite/packing upper sector moments at ell. The untwisted trace is at most z=A+2B+3C; every nonidentity tetrahedral seam is at most p_seam=A+2B. Separately cooling each physical Gibbs trace gives

    D=z^r, E=p_seam^r,
    tau=(D+11E)/12, tau0=(D+3E)/4.

D,E are rounded upward. They bound the total, trivial, and trivial-plus-complex masses at beta=r beta0. Their definitions retain the same physical temperature for all sectors.

The exact MPS104 shifted total Rayleigh quotient is

    R=H0_104/N0_104+104*a <0,

approximately -1.0938916430e-5. It supplies certified rational lower Boltzmann values

    v <= exp(-beta0*R),
    W <= exp(-r*beta0*R),

both greater than1. The first bounds one physical ground weight at beta0; the second bounds Z104 at cooled beta. Positivity and Jensen, not a presumed ground-state approximation or uniqueness, justify them.

For cooled transfer weights |lambda|^ell, their largest weight t satisfies Z104<=D*t^3. The code starts at t0=4/5, checking D*t0^3<W and2*t0>D. Thus the leading atom exceeds t0, is unique, and lies in the trivial sector. After removing it, the residual masses obey

    0<=x<=tau-t,
    0<=x+y<=tau0-t,
    0<=x+y+zeta<=D-t.

For exponent j>=1 their power tail is bounded by the maximum of

    x^j+2*(y/2)^j+3*(zeta/3)^j

over the same four polygon vertices from the accepted cooled-sector proof. Denote it R_j(t). It decreases in t. Consequently t^4>W-R_4(t0), and exact outward lower fourth roots iteratively improve t0. Each strict contradiction sum is checked against W, not against the older coarse anchor1.

The canonical spatial purity then satisfies

    S(52,beta) >= [1+R_2(t0)/t0^2]^(-2).

For the thermal seed let Q>=Z104(beta0) be the new Hermite/packing upper trace. The actual ground weight w0 is at least v. Its remaining-to-ground ratio is at most Q/v-1. Cooling yields

    T(104,beta) >= [1+(Q/v-1)^r]^(-2).

Using a lower v in the denominator is safe because the ratio decreases with v; all Q/v-1 values are verified positive. The resulting exact seed displays are S>=0.867427750539740 and T>=0.880322631774115. The small gain from the actual negative anchor is separated from the primary moment-majorant gain.

## Direct time-first windows: compatible basepoints, not a mislabeled seed

The independently accepted direct-time-first lemma requires a<=T(n,beta), b<=S(n,2beta), b>1/2. Our cooled construction instead directly supplies canonical S(n,beta) and T(2n,beta). These cannot be renamed a,b.

The exact exchange identity A^2 B=S^2 T and A,B<=1 allows inferred initial endpoints a>=sqrt(K), b>=K, where K=S^2T. These give the direct-window lower expression K*sqrt(2K-1), about0.37748 here; that particular inferred lower bound does not prove a gap. It is not an upper bound on the physical purity or a no-go theorem. The canonical signed-window bound at the same initial seed is about0.56988 and does prove a gap.

After the first spatial purification, however, the compatible time-first pair is available at base104 and physical beta567/25:

    a=T(104,beta) >= T,
    b=S(104,2beta) >= G(S^2 T).

The direct lemma then gives every integer104<=L<=208 a thermal purity at least a^2 sqrt(2b-1), about0.666744. The code separately checks this stronger bridge and the desired gap at the correct beta, without doubling it prematurely. It is a useful compatible improvement but is unnecessary for the already complete canonical certificate. Neither finite-window lemma can by itself repair a scalar iteration that dies before reaching a small-defect regime; this n52 route succeeds because the moment envelope improved startup.

## Exact recurrence, all early windows and asymptotic scope

Use the accepted canonical recurrence

    S_new=G(S^2 T), T_new=G(T^2 S_new),
    G(z)=1-(1-z)^2/(2z^2),
    n_new=2n, beta_new=2beta.

All endpoints are rounded downward on a10^-24 grid. Every argument/output is legal and positive. The exact signed-transfer finite-window lemma is checked at every state, covering

    [52,104], [104,208], [208,416],
    [416,832], [832,1664], [1664,3328].

These are all-integer intervals, not only even endpoints. For each lower thermal purity C>1/2, the rational exponential check exp(beta*19/5000)*(1-C)<C proves the gap and ground-state uniqueness. The smallest displayed initial C is about0.569880605451. The dominant transfer sign for odd lengths follows from the accepted all-integer trace identity and positive physical odd partition functions, exactly as in the reviewed bridge theorem.

At n*=3328,beta*=36288/25, the common defect is approximately0.000541540925895409, below1/100. The inherited small-defect theorem applies, and the exact check

    exp(beta*19/5000)*5*u <1

establishes the same gap for every integer L>=3328. The code additionally checks[3328,6656] as an overlapping consistency window. Together these claims cover every integerL>=52, with no missing earlier windows. The global claim stops there.

## Verification, limits and reproduction

Run python certify.py. It imports no eigensolver and makes no physical computation. Current cost is about0.8CPU seconds and12MiB on CPU0 under700MiB/600CPU-second limits. Directed rational power roots are checked by exact integer powers, and exponentials by Taylor polynomials with geometric remainder and outward repeated squaring. certificates.json contains the polynomial coefficients, signed endpoint choices through the full rational expressions, exact seeds, anchor bounds, recurrence states, window purities, and strict margins. INPUT_SHA256.json records all consumed sources; MANIFEST_SHA256.json seals the package.

explore.py and explore_old.py are floating proposal tools, not exclusion certificates. Their lack of a candidate below52 says nothing about all temperatures, all available moment methods, or all physical seeds. The current-operator exclusions at n<=24 concern a different fixed numerator/initialization recipe and are not used here. No root/GitHub files, accepted n54/56/60 package, or older assessment/review seal was modified. Independent review is required before promoting this new n52 claim.
