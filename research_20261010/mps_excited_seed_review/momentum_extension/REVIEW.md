# Independent momentum witnesses and exact spin completion

Model: uniform periodic spin-1 H_n=sum_j S_j·S_(j+1), unit coupling, even n, physical basis (-1,0,+1). The n=2 Hamiltonian retains both periodic bond occurrences. This review concerns n=24 denominator witnesses and the same fixed archived D26 Rayleigh numerator at length48. Earlier three-state and longitudinal review seals remain immutable.

## Displacement forms and a different full-H contraction

Write R_j=S_j+/sqrt(2), v_j=R_j ψ_24, C(r)=<v_0,v_r>, and K(r)=<v_0,H v_r>. Translation invariance of ψ gives the full Gram and Hamiltonian forms C(j−i) and K(j−i). All tensors and operators are real. Hermiticity and translation imply C(−r)=C(r), K(−r)=K(r); reflection invariance and an a priori SU(2)-invariant MPS are not needed. Hence the 13 displacements r=0,...,12 determine the complete 24×24 forms.

The producer contracts explicit two-site H-insertion tensors and accumulates open-chain bonds, adding the periodic seam separately. The independent engine deliberately does not read any two-site H tensor. It uses the exact one-site decomposition

h = M⊗M + R⊗L + L⊗R,

where M=Sz and L=R†=S−/sqrt(2). At each site, sources on the bra and ket are inserted into the local tensor before the physical operator contraction. This retains the correct noncommuting order when H overlaps one or both sources. The engine carries the norm product, an open-chain energy sum, and three pending single-site operator channels. The next site closes each channel with its partner operator. The seam is computed independently by placing an operator at site0, propagating through sites1,...,22, and closing the partner at site23. No translation multiplier is used for these nonuniform source states.

Every local norm and bond-source tensor in the frozen producer file is separately reconstructed from physical spin matrices and compared exactly (13 matrices). The independent contraction engine instead uses 16 one-site source/operator transfers built from that same explicitly checked local physics. This provides a different decomposition and different insertion bookkeeping for the full Hamiltonian. Global 676×676 indices replace the producer's rectangular auxiliary blocks. All relevant source/operator charge shifts are checked against the virtual labels.

The physical fixtures expand every word at n=2,4,6, construct each local raised state, apply the complete periodic H, and compute every C/K displacement. They verify all source overlaps and the doubled n=2 seam convention. The n=24 GMP outputs are compared integer-for-integer with every frozen displacement. The staggered sum also reproduces the previously independently sealed Φπ norm and H numerator, providing a cross-check against the original two-source polynomial calculation.

## Fourier normalization, phases, and zero modes

Let ω=exp(2πi/24), Φ_k=sum_j ω^(kj) v_j, and T v_j=v_(j+1). Then TΦ_k=ω^(−k)Φ_k. This explicit sign convention matters for labels but not for the equal k and24−k energies. The exact formulas are

||Φ_k||²=24 λ_C(k),    <Φ_k,HΦ_k>=24 λ_K(k),
λ_C(k)=sum_r C(r) cos(krπ/12),
λ_K(k)=sum_r K(r) cos(krπ/12).

The 24 factor is retained in unnormalized vector norms and cancels only in the Rayleigh quotient. The producer's saved norm-eigenvalue intervals refer to λ_C, not directly to ||Φ_k||². The independent output records both.

At this length the cosines lie in Q(sqrt2,sqrt3), with basis 1,sqrt2,sqrt3,sqrt6. The independent verifier collects each complete Fourier sum into its four exact rational coefficients before interval evaluation. It uses decimal-grid radical bounds with denominator10^60 and verifies each endpoint by squaring. It also checks the exact cosine addition recurrence in the four-dimensional algebra. This differs from the producer's termwise 160-bit interval sum and is tighter. Every independently obtained Gram, H-form, and Rayleigh interval lies inside the respective producer interval.

The k=0 coefficient vectors vanish exactly for both C and K. Since ||sum_j R_j ψ||²=24 sum_r C(r)=0, that vector is exactly zero and is omitted. It cannot be normalized or counted as a state. Every other k=1,...,23 has a strictly positive rational lower norm endpoint, so the Gram rank is exactly23. Distinct translation eigenvalues give exact orthogonality, even when energies happen to agree. The k=12 Rayleigh interval collapses to the exact previously audited staggered quotient.

## Original 48-state count

Each of the23 nonzero Sz=+1 momentum states has a spin-flipped Sz=−1 partner with the same norm, energy, and momentum because F commutes with H and translation. Adding ψ in Sz=0, momentum0, and the already certified longitudinal momentumπ state gives48 orthogonal states. Representatives k=1,...,11 have multiplicity4 (opposite momenta and spin flips); k=12 has multiplicity3, including the longitudinal state. These are trial-vector counts, not asserted energy-eigenvalue degeneracies.

## Exact finite-n24 singlet deduction and 70-state count

Here an exact SU(2) conclusion can be derived from the new zero-mode data; it is not assumed from a numerical approximation. Let R=sum_j R_j, L=R†, M=sum_j Sz_j. The local integer matrices verify

[R,L]=M,    [M,R]=R,    [H,R]=[H,L]=[H,M]=0.

The virtual charge rule already gives Mψ=0. The independently verified exact zero norm gives Rψ=0. Consequently

||Lψ||²=<ψ,RLψ>=<ψ,(LR+M)ψ>=0,

so Lψ=0 too. Equivalently the spin Casimir annihilates ψ; the nonzero n24 vector is an exact total-spin singlet. This finite-length statement does not assert the same property at uncomputed sizes and does not assert that ψ is an H eigenvector.

For each v_j=R_jψ, raising operators commute, hence Rv_j=0 and Mv_j=v_j. Therefore RLv_j=v_j. It follows for every i,j that

<Lv_i,Lv_j>=<v_i,v_j>,
<Lv_i,H Lv_j>=<v_i,Hv_j>.

The second identity uses [H,L]=0, not an H-eigenvector assumption. Moreover

Lv_j=[L,R_j]ψ=−Sz_jψ.

Thus the normalized lowering convention is exact: LΦ_k is minus the single-source longitudinal Fourier state. It has the same norm and Rayleigh quotient as Φ_k, total Sz zero, and unchanged momentum. In conventional unscaled notation L=S−/sqrt(2), so no factor2 is missing. These states retain bond≤52; one does not need a product construction of bond104.

There are23 positive-norm modes in each of the three Sz sectors. Different sectors are orthogonal, and within each sector distinct momenta are orthogonal. ψ has Sz0 and momentum0, absent from the tangent list. The total is 1+3×23=70. Grouped multiplicities are6 for representatives1,...,11 and3 atπ. The full quadratic-form equality and the local normalized lowering identities are also checked on every site of the n=2,4,6 physical fixtures.

## Necessary-condition scalar screens

The certified upper Rayleigh endpoint α_k^up yields a safe Jensen term exp(−βα_k^up). The denominator lower trace is exp(−βα0) times 1+sum_k m_k exp(−βg_k^up), with g_k^up=α_k^up−α0. These lower traces only bound from above the achievable input of the specified fixed one-Rayleigh numerator recipe. They are not upper traces and do not themselves initialize a successful bootstrap.

Using independently tightened Fourier endpoints, the scalar verifier independently checks every producer interval with the core's separately reviewed decimal-grid exponential enclosures and monotone joint-aware replay. It verifies that all closed intervals connect without a gap from1/2 to80; the trace-Jensen hot interval [0,1/2] and ground-only cold ray [80,∞) close the complete half-line. Warm intervals have width at most1/4, with1/64 refinement where needed. A claimed excluded box must independently exhibit finite sign failure for every permitted whole-cycle time-first delay and subsequent accepted canonical conversion. Optimistic target entrance and finite caps remain inconclusive.

The 48-state screen leaves only [533/64,679/64] unresolved. The derived 70-state screen leaves only [539/64,339/32] unresolved. All other β≥0 are excluded for the specified fixed recipe. Neither remaining interval certifies actual feasibility, a true physical trace ratio, a spectral gap, gaplessness, or a universal minimum seed size. The inherited even-base transfer/purification identification and accepted conversion are the same premises as the core review.

## Dimension and cost accounting

The denominator Hilbert dimension is 3^24=282429536481. The numerator at48 has dimension 3^48=79766443076872509863361 and retains one fixed D26 MPS. The transverse orbit has24 generators and rank23; the retained spans have48 and70 dimensions after orthogonal spin/momentum completion. Individual single-source MPS bonds are at most52. Auxiliary transfer dimension676 and maximum charge-block side162 are distinct from all these dimensions.

No physical support or Hamiltonian matrix is expanded above n=6. No eigensolver or energy optimization is used. Exact Fourier algebra diagonalizes only the circulant trial Gram and H forms. All replay processes use CPU1. Displacement and physical-fixture processes use700MiB address-space caps; the separately reviewed scalar primitive retains its1GiB cap. Actual RSS is recorded for each component. A two-displacement independent benchmark and a conservative cost gate precede the remaining contractions. RESOURCES.json records actual costs; compiled binaries are reproducible from source and are not required for the seal.
