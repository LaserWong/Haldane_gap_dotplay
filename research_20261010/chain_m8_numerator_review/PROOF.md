# Independent M8 numerator Krylov audit

Updated 2026-10-10 18:07 EDT (America/New_York) / 22:07 UTC.

## Physical inputs and exact action

The Hamiltonian is the periodic alternating spin-one chain at g=1/4, with eight unit strong bonds and eight weak bonds. There are 16 physical spin-one sites, eight dimers, and full Hilbert dimension 9^8=43,046,721. Strong-dimer shifted energies are 0,1,3; their orthogonal rational Clebsch–Gordan columns have weights 3,2,2,2,1,2,6,2,1.

The independent physical kernel is reconstructed from explicit spin-one matrices, not imported from producer mathematical code. Its exact metric Hermiticity is checked. Every weak edge, including the periodic closing edge, is included. Let A=144H8. This integer scale clears every physical weak-kernel denominator at g=1/4, while retaining the unshifted strong energy −16+sum(e_i).

The old two trial vectors u,v are read from their sealed original NPZ files. Their common 43,294-state basis is checked to be identical and duplicate-free. Integer coefficients are converted to Python integers before any multiplication. The starting vector is independently rebuilt as ψ=a u+b v with the two saved integer coefficients; b is nonzero. Both packed input files, their kernel headers and every coefficient are compared to this reconstruction.

Every dimer label occupies four bits, and eight labels use 32 bits. Labels are restricted to 0,…,8 and packed keys to [0,2^32). Full physical action independently constructs and checks

φ=Aψ, with 243,475 nonzero configurations;
η=A²ψ, with 935,927 nonzero configurations;
ξ=Au, with 243,438 nonzero configurations.

Each entire output dictionary is compared entry-by-entry against the saved files, with duplicate, out-of-range, missing-state and coefficient checks. Zero sums are removed only after all physical contributions have accumulated. No occupancy, excitation-energy, support or symmetry truncation is applied to these actions. The first, second and auxiliary actions traverse 2,555,752; 15,543,346; 2,555,752 weak-kernel transitions, respectively.

These counts are supports in the complete orthogonal dimer basis. They are not physical eigenvalue counts, linear trial dimensions, or MPS bond dimensions.

## Integer overflow controls

The independent implementation uses Python arbitrary-precision integers for every coefficient, action accumulation, overlap and energy sum, and Fraction for certificate matrices. NumPy is used only to load immutable arrays; no NumPy fixed-width multiplication or matrix contraction evaluates large coefficients.

The second image contains 107-bit coefficients. The first image already needs 95 bits. Thus a fixed 64-bit coefficient representation would be invalid. The exact full fifth moment is independently recomputed with unbounded integer accumulators. The producer uses GMP integers, but acceptance does not rely on its binary or overflow behavior.

Packed states fit 32 bits; the maximal valid packed word is 0x88888888. Metric products are bounded by 6^8=1,679,616. Local integer kernel coefficients and 144 times the strong energy fit signed 32 bits. These small structural ranges are independently checked and are separate from the unbounded amplitudes and moments.

## Full contractions and the fourth trial direction

With metric inner product, let N=<ψ,ψ>. Exact physical actions give

q1=<ψ,Aψ>=<ψ,φ>,
q2=<φ,φ>,
q3=<φ,η>,
q4=<η,η>,
q5=<η,Aη>.

Hermiticity proves qj=<ψ,A^jψ>. Thus physical normalized moments are μ_j=qj/(144^j N), j=1,…,5.

The verifier recomputes q5 by enumerating every physical directed weak transition from every η configuration, together with its strong diagonal term. This checks 60,872,321 weak transitions. Contributions whose target lies outside η's bra support are exactly zero in <η,Aη>; omitting their zero scalar contribution is not a truncation of a residual. No full A³ψ vector is needed for this first moment. A separate complete directed contraction checks the analogous auxiliary ξ moment. All norm and moment linkages in the saved full/second/old-direction records are verified.

The four trial columns are T=(ψ,u,φ,η). Every entry of G=T*T and H_T=T*H8T is reconstructed. For its first three rows, H8ψ=φ/144, H8u=ξ/144 and H8φ=η/144 give the exact mixed matrix elements. Hermiticity supplies the matching column entries. The final diagonal is <η,H8η>=q5/144. Therefore every matrix element is a complete physical first-moment contraction, including those involving the H²ψ direction.

No full H³ψ output, filtered-state residual bound, largest-seed spectral lower bound, isolated low band, or omitted-eigenstate count is inferred. The four columns form an optimization space for a single retained Rayleigh numerator term, not four certified physical eigenstates.

Since b≠0, span{ψ,u}=span{u,v}. The full space is precisely the union of both old directions and Hψ,H²ψ. Exact positive Gram pivots prove its dimension is four.

## Rational Rayleigh trials and entire-span exclusion

The saved four rational coefficients c are evaluated directly:

ρ_new=(c*H_Tc)/(c*Gc).

The norm is strictly positive, the quotient matches the saved exact rational value, and the improvement over the original ψ is approximately .0003036764441946725. The remaining δ=ρ_new−2ρ4 is approximately .0153224674126672, where ρ4 is the same independently certified M=4 ground Rayleigh normalization used in the prior obstruction.

Let λ=2ρ4+19/1250. Exact rational LDL elimination verifies both G>0 and H_T−λG>0. It follows that

(c*H_Tc)/(c*Gc)>λ

for every nonzero real or complex coefficient vector c in this four-dimensional span. Hence no different coefficient optimization in this space can meet δ<.0152. This is a lower bound on Rayleigh quotients in the stated span, never a lower bound on the full physical M8 ground energy.

The independent moments also replay the reported two-dimensional trial span{ψ,Hψ} and three-dimensional span{ψ,Hψ,H²ψ}. Their saved rational coefficient quotients, moment matrices and exact positive target pivots are checked. Both are subspaces of the four-dimensional space, so their entire-span failures also follow directly from the four-dimensional exclusion. Floating eigenvector searches are only coefficient proposals and are not used in acceptance.

## Composition with the prior all-temperature obstruction

The sealed independent rank195 review proves a necessary condition for this specific route: a one-term M8 Rayleigh numerator must satisfy ρ8−2ρ4<19/1250 to pass the specified initial time-first purification, canonical transport and mandatory first [8,16] signed-transfer window, even with an exact M4 trace. Its physical spin-one triplet bound and all-temperature interval proof cover every valid M4 trace upper bound. The current provenance check verifies that review seal and the exact target before composing results.

Every vector in the four-dimensional space violates that necessary condition. Consequently this finite family cannot certify the early window for any β≥0, irrespective of coefficient optimization or denominator refinement. A new sufficient-path temperature scan is not needed to establish this scoped failure.

No positive gap at .25 is claimed. The result does not exclude trial states outside this space, multiple independently justified numerator contributions, different early inequalities or orderings, an independent early-size bridge, or different seed geometry. It neither bounds physical purity from above nor proves that the physical chain is gapless. The completed rank67 and rank195 seals are preserved, and separately evolving pair-orbit extensions are outside this audit.
