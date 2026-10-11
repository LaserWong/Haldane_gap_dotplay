# Independent smaller second-input initialization review

2026-10-11 02:25UTC /2026-10-10 22:25 America/New_York.

## Verdict and scope

ACCEPTED for the untwisted periodic uniform spin-one Heisenberg Hamiltonian, bilinear coefficient1:

- gap at least31/1250=.0248 and unique ground state for every integer L≥34;
- gap at least49/2000=.0245 and unique ground state for every integer L≥32;
- gap at least179/10000=.0179 and unique ground state for every integer L≥30.

These are three independently initialized canonical chains at beta0=49/4, using their own68-,64-,60-site anchors respectively. Their coverage starts equal their initialization sizes. They may be combined as nested bounds: .0179 on30..31, .0245 on32..33, .0248 on every L≥34. This differs from extending a larger initialization by a separate finite-window bridge. No minimality, below30 exclusion, or n28 conclusion is supplied. Earlier n48/n50 fixed-recipe exclusions concerned different thermal data and do not constrain these second-input constructions.

Producer seal: fcf4d2c7f838a8ee154f297549f3049a93b49cae30e758534edc9c3dc2d74a84. All three rows and every advertised signed long-moment majorant were independently replayed. Floating search history is not accepted as proof of optimality or failure outside the tested candidates.

## 1. Physical inputs and independent fresh anchors

The18 beta49/4 thermal inputs, including odd lengths4..12 and I/P seams, have already been physically reproduced and independently accepted by uniform_second_thermal_full_review, manifest792127565ad16526eeaa61add62bcc15db499578fc9d2157f11df27848867b94. That review explicitly maps exact physical error intervals to the refined signed moment intervals used here. No new thermal computation or replacement premise is used.

rebuild_d26.py reconstructs all three real26-by26 site tensors directly from the fixed D26 representation labels and rational/integer coefficients. It constructs the transfer matrix T=sum_s A_s tensor A_s and the two-site physical insertion O entrywise. In the weight basis the spin-one bond has diagonal s*t and unit ladder-exchange coefficients. Its charge-difference blocks are reconstructed rather than copied from the producer integers. Freshly rebuilt blocks match the previously physically accepted original blocks byte for byte. Independent direct amplitudes at lengths2 and3 reproduce both their norm and their TOTAL periodic Hamiltonian numerator; this checks the transfer and energy conventions.

The inspected, previously sealed reviewer engine uses sequential exact GMP powers, independently of the producer's binary-power engine. A fresh48-site benchmark exactly matches accepted integers before the60/64/68 batch. All six new norm/energy integers match the producer. The output convention is N0_L=Tr(T^L)>0 and H0_L=L Tr(T^(L-2)O), already TOTAL energy. Therefore the shifted quotient is H0_L/N0_L+aL with a=700741/500000, without another factor L. Its exact sign is negative at each60,64,68. Displays are approximately −1.18579855e−5, −9.28394650e−6 and −8.32217861e−6; only the exact signs authorize use.

D=26 is trial bond dimension, the trial span is one-dimensional, and the physical Hilbert dimension is3^L. Neither26 nor676, the norm-transfer dimension, is the physical thermal-transfer rank. The variational principle supplies a negative shifted energy, hence Z_(2n)(b)>1 at every b>0. Ground uniqueness is not an anchor premise.

## 2. Signed global-domain moment inequalities

The inherited sectors J and N satisfy full trace J+3N, with moments lambda^k for k4..12, not powers of lambda squared. Odd moments retain their signs. The reviewed directional support caps bound both complete exterior rays; this package does not alter them.

For every one of the26 advertised even-k bounds, the reviewer independently constructs p(x)-x^(k-4), where p has degree8 and exact rational coefficients. It maps the entire closed signed support interval to[0,1], forms exact full-degree Bernstein coefficients and recursively splits by de Casteljau. Every leaf has nonnegative coefficients. Thus x^4 p(x)≥x^k everywhere on support, including zero and the negative half-line. No division by x, sampling, floating extrema or truncation of spectral rank enters this proof. All independently computed leaf counts and depths match the certificate.

Summation is valid for the countable spectrum: finite fourth/twelfth moments bound absolute intermediate powers by |x|^4+|x|^12. A positive coefficient uses the upper endpoint and a negative coefficient uses the lower endpoint of the corresponding signed moment. The reviewer reproduces each upper bound exactly. Shared I/P correlations do not invalidate simultaneous interval enclosures; independent attainability of every adverse endpoint is not assumed.

## 3. Packing and the positive leading atom

For y_i in[0,h], sum y_i≤m and r≥1, convex redistribution in finite lists proves sum y_i^r≤floor(m/h)h^r+(m-floor(m/h)h)^r. The expression is monotone in m; finite-subfamily limits extend the inequality to countable lists. Apply y=lambda^12, retaining N multiplicity3. The minimum of this packing upper bound and a certified polynomial upper bound is valid. Length60 uses packing, while64/68 also use their available polynomials.

With mJ,mN the twelfth-moment upper bounds, each candidate ell satisfies

    pack(mJ,ell^12,2n/12)+3 upper(N_(2n)) < 1.

If all J eigenvalues had modulus≤ell, this would contradict Z_(2n)(beta0)>1. Therefore a J eigenvalue has modulus>ell. The reviewer checks ell exceeds the negative-J support cap and the entire N modulus cap, so this atom is positive and dominates N. Removing one occurrence leaves residual twelfth mass R≤mJ−ell^12. The exact check0<mJ−ell^12<ell^12 excludes a second atom of that size and proves unique modulus dominance, without finite-rank assumptions.

For even n, let B_N(n) be the chosen upper N moment and Q the certified full2n trace upper bound. Keeping the positive dominant numerator term and bounding the residual gives

    S(n,beta0) ≥ [1+((mJ−ell^12)^(n/12)+3B_N(n))/ell^n]^-2,
    T(2n,beta0) ≥ Q^-2.

The second inequality uses Z_(2n)(2beta0)>1 from the same physical anchor. Exact integer nth-root bracketing at a10^-140 grid independently encloses every rational power, including17/6,8/3 and5/2. Raising both rational endpoints to the integer denominator verifies their direction. The reviewer uses more precise independent enclosures than the producer's10^-100 grid and checks every saved seed endpoint is conservative.

## 4. Staggered iteration, odd lengths and complete coverage

The inherited analytic theorem uses S(n,beta),T(2n,beta). Its sequential update is

    S_new=G(S^2 T), T_new=G(T^2 S_new),
    G(z)=1−(1−z)^2/(2z^2),

followed by doubling n and beta. The second update uses the NEW spatial value. Monotonicity on(0,1] justifies conservative rounding. Every saved step, positivity domain, coordinate, temperature and endpoint is independently checked against its exact expression.

At each stage let K=S^2 T>1/2, w=(1+sqrt(2K−1))/2, rho=(1−w)/w and d=T/(1+rho^2). The accepted signed-transfer interpolation yields a physical purity lower bound

    C=(1−rho) min(S sqrt(d), d)

for every INTEGER length in[n,2n], including odd lengths. Its leading-sign argument is legitimate because the official physical identity Tr(X_beta^L)=Z_L(beta) holds for every integer L≥4, with no odd twisted-chain substitution. Purity>1/2 forces unique modulus dominance; a negative leading eigenvalue would eventually make odd physical traces negative. Subleading eigenvalues may remain signed. This is precisely the already reviewed finite-window lemma; no entrywise transfer positivity is substituted.

For each claimed gap delta, the reviewer proves exp(beta delta)(1−C)<C by independently directed Taylor/exponential bounds. The saved windows have no holes: the next start is the previous doubled size. The respective asymptotic starts are17408,16384,30720. All have terminal beta6272,6272,12544 respectively. The terminal defects u=max(1−S,1−T) satisfy u≤.01 and5u exp(beta delta)<1. The inherited small-defect recurrence u_new≤5u² and its finite-window control therefore cover all remaining lengths at the same delta. The exact domain constants are rechecked. Uniqueness follows from the resulting purity bounds, rather than being assumed to cool a ground-state contribution.

## 5. Resources, tests and provenance

Fresh reconstruction, benchmark and anchor contractions total40.09145CPU seconds, below the60-second scientific budget, with13.6MiB anchor peak memory. The external100MiB/60CPU-second hard limits cannot be raised by the reused executable; it remains single-coreCPU5. The independent scalar replay uses9.91CPU seconds and17.8MiB onCPU4, below60CPU seconds/256MiB. No imported producer code is executed. All producer files are read as data, source or seal inputs.

Nineteen exact adversarial fixtures cover fractional-power direction, negative-base rejection, global polynomial endpoint failure, signed moment endpoint selection, invalid G domains, inflated updates, staggered labels, coverage holes and single-bond/total-energy confusion. Full source and dependency digests are in ANCHOR_INPUT_SHA256.json and SCALAR_INPUT_SHA256.json. Original physical tensor/source attribution remains in the unchanged prior packages. No root, producer, campaign ledger or prior seal was modified.
