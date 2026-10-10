# Independent pair-sector and block-numerator review

Updated 2026-10-10 18:18 EDT (America/New_York) / 22:18 UTC.

## 1. Physical conventions and the complete five-dimensional bare sector

The periodic alternating spin-one chain has eight dimers, unit strong coupling and g=1/4 on all eight weak edges. Its full dimension is 9^8=43,046,721. Dimer labels 0,…,8 are the accepted orthogonal rational Clebsch–Gordan columns; shifted energies are 0,1,3 for spin 0,1,2, with degeneracies 1,3,5. The integer physical action is A=144H8. The independent checker copies the previously sealed independent physical-action implementation, not producer mathematical code.

At weighted dimer energy E≤2, there are only vacuum, one-triplet and two-triplet configurations. The vacuum contributes one singlet. A single triplet has total spin one and contributes no singlet. For each of the 28 unordered pairs of occupied cells, two spin-one triplets have precisely one total-spin-zero coupling. Thus the E=2 singlet sector is spanned by these 28 pair singlets.

On the periodic eight-cell ring, the unordered pairs have four translation orbits, classified by separations 1,2,3,4, of lengths 8,8,8,4. The two-spin-one singlet is symmetric under factor exchange, so the opposite-pair stabilizer introduces no sign. Translation invariants therefore have dimension four. Including vacuum gives the complete five-dimensional translation-invariant singlet sector at E≤2. A quintet has energy three and does not belong to this sector.

For an occupied pair i,j, exact coefficients on triplet labels (1,3),(2,2),(3,1) are +1,−1,+1. Each orbit sums once over distinct unordered pairs. The verifier independently enumerates all 28 pairs, proves the orbits disjoint and exhaustive, reconstructs all five vectors, and checks their norms:

6561,69984,69984,69984,34992.

Their supports are 1,24,24,24,12 and are pairwise disjoint, so the vectors are orthogonal and independent. Total magnetization is zero; exact total raising and lowering both annihilate every vector. The raising/lowering matrices are reconstructed from physical one-spin operators rather than inferred from floating eigenvectors.

Cell translation rotates the eight dimer labels. Physical reflection reverses their order and exchanges the two physical spins in every dimer. The local exchange sign is −1 on triplets and +1 on singlets/quintets. Direct exact checks give translation and physical-reflection eigenvalues +1 for all five bare vectors. Every invariant singlet orbit in this E≤2 sector is reflection even, so no additional reflection-odd singlet direction is missing.

## 2. Exact full actions and cross contractions

All five full A-images are reconstructed without any weighted-energy or support truncation. Their union has 1961 nonzero dimer configurations, including all leakage. Each entire sparse image is compared to the saved file. New selected directions are obtained only by division by the positive integer gcd of all image coefficients, which preserves their span. Every subsequent full image is independently reconstructed too.

The previous four physical columns are ψ,u,Aψ,A²ψ. Their complete coefficient files and independently checked four-dimensional Gram/H blocks are reused only after the old review seal is verified. The old columns are read in full for overlap evaluation; saved restricted overlap dictionaries are checked against those complete files.

For a new column v with exact full image Av, the verifier computes every new Gram element <v,w> and every new Hamiltonian element <Av,w>/144. Physical metric Hermiticity gives the opposite orientation. When both full actions are explicit, the checker additionally verifies <Av,w>=<v,Aw> directly for every pair of new directions and for the available old actions. No full A³ψ vector is required for a cross element with A²ψ: the new direction's full action and Hermiticity determine that element exactly.

The old 4×4 blocks remain unchanged. Every larger Gram and Hamiltonian entry is compared with the independent contractions. This is numerator-only first-moment information. No filtered residual, isolated spectral band or full-space lower eigenvalue is inferred.

## 3. Exact ranks and block selection

Positive exact Gram pivots establish that the two original directions plus the five bare vectors have rank seven, and the old four-dimensional space plus those vectors has rank nine. Thus their intersections with the complete five-dimensional bare sector are zero as full physical subspaces, irrespective of overlap between their low-energy projections.

At the first image extension, each of the five primitive A-images is appended and tested by exact Schur/Gram pivots against all previously selected columns. The vacuum image is dependent. Explicitly, if b1 denotes the nearest-pair orbit,

A|vac>=−2304|vac>+36b1,

so its primitive version is −64|vac>+b1. The other four candidate images have strictly positive residual Gram pivots and increase the rank from 9 to 13. All four images of these newly selected directions are independent in the second extension, giving rank 17. The reviewer verifies every candidate, primitive vector, exact zero/positive dependence pivot, selected ordering and complete next action.

The new bare vectors, selected image directions and all their saved next images have exact spin zero, translation+1 and physical-reflection+1; these quantum numbers are checked directly rather than assumed from H-invariance.

Important scope clarification: the inherited ψ and u packed rational vectors have M_z=0 but fail exact translation/reflection and total-raising/lowering equalities. Consequently the combined 9D/13D/17D spaces are not wholly exact singlet/even sectors. The exact quantum-number statements above apply only to the newly constructed pair-derived directions. This does not weaken any Gram, physical Rayleigh or entire-span bound: those arguments apply to arbitrary physical vectors and do not require a fixed symmetry sector.

## 4. Exact Rayleigh inputs and entire-span target bounds

For each rank 9,13,17 space, the saved rational coefficient vector c has positive norm c*Gc. The verifier independently recomputes its energy numerator c*Hc and quotient ρ=(c*Hc)/(c*Gc). The exact saved values and shifts relative to the same certified M4 Rayleigh normalization match. Their approximate δ=ρ8−2ρ4 values are:

rank 9: .015311537528561982;
rank 13: .015308489680354413;
rank 17: .015304451528169765.

For λ=2ρ4+19/1250, rational elimination proves H−λG>0 on every whole trial span. Along with G>0, this gives Rayleigh quotient>λ for every nonzero real or complex coefficient vector in that span. It is not a lower bound on the full M8 ground energy.

The rank 17 numerator_input.json is additionally checked against block_2.json: its source hash, physical model size, rank, exact norm, exact energy numerator, Rayleigh quotient and δ all match the independent evaluation. Therefore it is a reusable single Rayleigh numerator input. The reviewer emits certified_numerator.json for this purpose. Trial rank 17 does not mean seventeen retained physical eigenstates or numerator trace terms.

## 5. Recipe scope and the new direct time-first window

The previously accepted δ<.0152 necessary condition applies only to the old canonical-transport first-[8,16]-window recipe. The positive target pivots above exclude all coefficient choices in these finite spans from that old recipe, even with exact M4 trace, by composition with the unchanged rank-195 review.

A new proposed direct time-first window bound a²sqrt(2b−1) is a different scalar argument and is being reviewed separately. The old target theorem does not apply to it. This package does not establish its validity, exclude its success, or provide an all-size positive gap through it. The exact rank 17 numerator may be reused in that separate work without carrying over the old recipe's failure conclusion.

No physical no-gap statement, all-numerator-state exclusion, or full-space spectral lower bound is asserted. Different vectors, additional numerator contributions, different bridges and different scalar routes remain outside the old finite-span obstruction. Previous seals are preserved, and this review changes no producer, root or remote files.
