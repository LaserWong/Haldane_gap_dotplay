# Independent continuous bilayer extension to g = .10

Review date: 2026-10-10, America/New_York (EDT, UTC−4). All ten closed pieces in [9/100,1/10] pass with uniform gap at least 2190412273/250000000000 = .008761649092. The sealed predecessor plus these pieces gives 66 closed pieces covering [0,1/10], gap at least 486442811/250000000000 = .001945771244, for every integer L≥2. There are 46 checked finite windows (36 needed before the analytic tails), 60 short-size rows and 480 odd modes; the largest analytic onset is L=256. REVIEW_STATUS.json records the final immutable acceptance.

## Scope

Ordinary spin-1/2 periodic square bilayer, rung coupling 1, two straight intralayer exchanges g, no crossed bonds; positive-direction periodic multiedges retained. H′=H+3N/4=Q+(g/2)A. The claim concerns every real coupling in the listed closed intervals and every integer square side L≥2, with a unique finite-volume ground state. It does not concern arbitrary rectangles, infinite-volume uniqueness, physical-gap monotonicity, or a critical coupling. This is an analytic argument with exact-arithmetic certificates, not a proof-assistant formalization.

## Independent physical replay and provenance

The previously sealed interval .09 review is 09937dcdee71981b15990ff2696a72eafb5d4967e6cbae9d71392c9b802d2334. The complete 8×4 residual review is 47ca2166342038a845f45d774bd9e2d91429496235df6e6d0fc39fb678a2b081. Every file in both seals, the complete review's inputs and dependencies, and the new producer's direct inputs and inherited seals are hash-checked before importing any mathematical helper. The frozen producer is 833a50bbd764c15c2ef63300c95cb93c859d5c8101bfa7703fc3c6161ef0e487. All its files are snapshotted. Producer Python is neither imported nor executed.

The 8×4 witness is exactly the independently accepted integer vector in the 43-column B,L,U basis, U=R+M, supported in q=0,2,4,6. Decomposing U into homogeneous q4 R and q6 M gives 57 bookkeeping columns, not 57 independent vectors. The replay independently rebuilds G, Q, Q², A and QA+AQ expectations from accepted physical contractions. At g0=1/10 the accepted complete second moment includes q8 creation and coherent q4/q6 cross terms; with t0=g0/2,

A² expectation = (norm × second(g0) − Q² expectation − t0 × (QA+AQ) expectation)/t0².

Because H′(g)=Q+(g/2)A exactly, this determines every coefficient of the full second moment for this fixed vector, without interpolation assumptions. The mean is affine; the complete variance is quadratic. Every exported coefficient, norm and trial coefficient is checked. The variance leading and constant coefficients are positive and its discriminant is strictly negative. The nonzero complete residual is not a projected residual. Production q8 supports are not re-enumerated here; their complete contribution is an explicitly pinned accepted physical premise.

The 4×4 denominator's physical basis, complete moment polynomial and construction are unchanged, while its numerical rational witness may change with interval center. The 8×4 odd physical family is unchanged. The 8×8 numerator is rebuilt from the accepted constant Gram and affine Hamiltonian matrices; every new fixed integer vector has positive norm and exactly checked affine Rayleigh coefficients. Its single contribution follows from convexity of exp(−βH′). No largest-seed full residual or unverified extra numerator level is used.

Dimension bookkeeping:

- 4×4 rungs: 32 physical spins, full dimension 2^32, ground search 11, odd directions 48, total search-plus-band 59, retained denominator levels 49.
- 8×4 rungs: 64 physical spins, full dimension 2^64, ground search 43, odd directions 96, total search-plus-band 139, retained denominator levels 97.
- 8×8 rungs: 128 physical spins, full dimension 2^128, search 43, retained numerator contribution 1.

Ground search and odd spaces are disjoint parity sectors, so their dimensions add; a ground search rank is not a retained level count.

## Rigorous coupling-uniform Temple bounds

For N=16 or 32 put C=3N/8 and r_q(g)=C(2g−1)+(C+q)sqrt(1−4g). Its difference from the affine mean rho(g) is concave on [0,.1]. Therefore the smaller of its two exact endpoint values bounds the entire closed interval below. Replacing each endpoint square root by the checked downward rational square-root enclosure only weakens the lower bound. The variance is convex, so the larger endpoint variance Vmax bounds it above everywhere. Diagnostic interior points are additional tests, never the proof of uniformity.

Two distinct positive margins are required. The global ordered reference gives λ₂≥r₁. A singlet even trial mean rho<r₁ produces a level below r₁ and identifies the unique global ground. Separately, the ordered reference gives λ_(3N+2)≥r₂. The N positive Fourier Gram modes in each of three spin projections give 3N independent odd Ritz states uniformly below r₂. Together with the even ground they exhaust the possible 1+3N levels below r₂. Thus the even-singlet sector has exactly one level below r₂. Only in that sector may Temple use r₂. The uniform lower energy is rho−Vmax/D₂, with D₂=min(endpoint downward r₂−rho)>0. Merely checking an even cutoff would not establish global ground identity; both margins are replayed explicitly.

Every odd affine mean and complete convex variance, including q5 leakage, is reconstructed with exact Q(sqrt(2)) Fourier arithmetic. Directed 160-bit endpoint enclosures establish all odd Temple denominators, widths and relative lower energies. Every norm and momentum is checked, preventing lost or duplicated modes. The 3N odd levels plus the ground are counted once. The omitted spectral tail remains the positive oscillator overcount with multiplicities binom(3N+q−1,q), q=2,…,N; these are not physical hard-core shell counts. All ground, band and omitted-tail exponentials are bounded outward.

## Correlation, joint identities and complete size coverage

Before minimizing in g, the exact affine combinations 8rho16−2rho64, 16rho16−4rho64, and 4rho32−2rho64 are formed. The extensive shifts cancel identically. Their common-coupling endpoint minima, together with complete denominator trace uppers, give the directed initial joint ratios. No separate extremization loses the correlation.

The scalar function is AST-identical to the previously accepted independent interval function except for its declared coupling domain; only the physical callback for the 8×4 ground polynomial is replaced. Every rounded recurrence state, sequential update argument, route merger, finite window and analytic small-defect witness is recalculated. We additionally check all explicit physical base labels and canonical/permuted edge endpoints. A formal partition-function exponent ledger establishes that both orderings at (n,n,β) telescope to the same product Z(2n,2n,2β)/Z(n,n,β)^8. A stale joint bound from another physical base is rejected.

The finite windows start at L=8 and include all integer sizes to the next doubled side. Every required window is included in the final minimum. The final redundant window is also replayed and overlaps the analytic tail. The terminal u≤1/500 condition and exact exponential gap witness establish the all-larger-size bound; thermal purity above one half forces a single ground state.

For each interval, L=2,…,7 is separately covered by the vacuum trial Rayleigh zero and positive r₁ at the high coupling endpoint. The periodic graph is freshly rebuilt: sum of squared edge multiplicities is 16 at L=2, and 2L² thereafter. The derivative of this explicit reference formula is nonpositive on the coupling range, so this endpoint bounds each complete interval. No physical-gap monotonicity is used. Exact adjoining rational endpoints cover [9/100,1/10] with no gaps; only after every interval passes is its minimum joined to the sealed [0,.09] bound.

## Reproducibility and adversarial checks

Run bash REPRODUCE.sh. It verifies the immutable review manifest before and after executing fresh exact audit and corruption tests into a separate unsealed directory. No eigensolver is used. BLAS thread counts are one, address space is capped at 1 GiB, and CPU6 is selected when permitted. All generated writes remain under this review. The extracted project has no Git metadata; neither project root, producer directories nor GitHub are modified.

The adversarial suite includes complete-residual coefficients, norm and fixed witness, q8 support, separate global-ground and even-singlet margins, odd leakage and bands, trace tails, correlated exponents, stale-base joint products, physical edge labels, finite windows, short-size multiedges, numerator rank/count conflation, interval holes and missing endpoints. See results/adversarial_rejections.json for every rejected corruption.
