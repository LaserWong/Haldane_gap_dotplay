# Independent complete58D residual-direction review

## Acceptance
PASS: the new full8×4 row has been independently contracted over every4495 fixed-origin q4 support and169911 fixed-origin q6 support. All174 G/H200/H200² entries match the sealed producer complete row. All290 derived coupling-polynomial row entries match. The complete58D Gram matrix is positive definite and the116D residual block-Gram atg=.11 is positive semidefinite. These are physical matrix results; no new ground-energy endpoint or all-size gap is claimed.

Producer package: bilayer_residual_direction_production_run, seal0801d23cbf02b1951fdcd6bc2fefe5e746f88e09fc96d793d9b90d5dc944be00. Producer complete-row hashbea723c7012a0992515c1072f6cdccd8eaf97d6a58e42317358022a1a12580f6.

## Independent physical implementation
The reviewer extended its previously accepted independent matching/bond-action engine, not the producer kernel or include files. It constructs the perfect-matchings algebra, loop Gram factors3^loops, local swap-minus-contraction spin action, hopping and creation/annihilation directly. Old L=C†B, R=DL and M=C†L channels are independently rebuilt. The new fixed vector is T=ΣcR_j C†R_j+ΣcM_j D6M_j, with all28 saved integer coefficients independently checked against2^48.

The engine independently computes T, CT, DT and KT, K=[C,C†]. K includes positive empty-bond terms, negative occupied-bond contraction and both signs of shared-vertex two-bond terms. On4×2, every nonzero Cartesian amplitude of all four vectors agrees with the separately constructed full4^8 physical fixture. All complete cross moments agree there as well. A separate full fixed-origin4×2 replay verifies exact N/4,N/6 normalization before the large pass.

The full8×4 pass covers all supports, including76,566 supports where all old M channels vanish but T does not. Generic T lookup is never restricted to old M-active supports. All169,911 scalar cache entries are populated. Every processed q6 support is compared to uncached T construction and all six translations to an occupied origin, totaling1,019,466 anchor checks. Cache relabeling uses independently constructed perfect-matchings permutations and combinadic indexing.

## Complete second moments and an independent cross orientation
With H200=200Q+11A, H200T has q4 component11CT, q6 component U=1200T+11DT and q8 component11C†T. Thus J_TT=||U||²+242||CT||²+121<T,KT>. The full q8 norm is exactly||CT||²+<T,KT>, and is strictly positive.

Mixed L and R entries are formed by their separate q4/q6 components. For an old M column, the reviewer uses
J(T,M)=242<CT,CM>+<U,1200M+11DM>+121<KT,M>.
The producer instead contracts121<T,KM>. These agree globally because K is self-adjoint. This opposite orientation is deliberately independent and avoids reusing the producer old-M commutator contraction. Their individual partial-support sums need not agree; the completed normalized physical rows do. No q8 sector is omitted, and no projected A²/H² is substituted.

For every translation-invariant support density, the fixed-origin sum is q/N of the complete sum. The reviewer keeps q4 and q6 accumulators separate, multiplies by N and verifies exact divisibility by4 or6 before adding. Both full support totals are asserted before this normalization. Progress checkpoints are explicitly partial and are not resume/completeness certificates.

## Exact arithmetic and bounds
The inherited independent old-family additions check signed32-bit channel bounds. New scalar channels use checked signed128 addition and multiplication. The conservative reviewed B=2^84 bound gives |DT|≤924B, |KT|≤20172B and |CT|≤5760B; U≤11364B. Gram precontraction sums at most15 terms with coefficient≤27, still safely within signed128 even for KT. Each full bilinear product is converted to GMP before multiplication and accumulation. Coefficients are parsed with checked arithmetic and bounded by2^48. No floating arithmetic enters any physical matrix entry.

## Coupling polynomial and cached independent consistency
T has occupation6. For column occupation q_j, recover
A_j=(H200_j−1200G_j)/11,
A²_j=(J200_j−1440000G_j−2200(6+q_j)A_j)/121.
All divisions are exact integers. H(g)=Q+gA/2 and H²(g)=Q²+g(QA+AQ)/2+g²A²/4 then give the complete new polynomial row. The old57×57 blocks are copied unchanged from the independently accepted complete split-matrix review. Every occupation grading identity is checked across the assembled58D matrices.

A separate cached derivation reproduces the entire new Gram row: its M cross entries come from cR·A(R,M)+cM·A(M,M), and its self norm comes from accepted R6R6, R6M6, its transpose, and M6M6 blocks. The full new Gram matrix has58 positive exact LDL pivots. The last pivot is the strictly positive Schur norm recorded in audit.json, certifying an additional independent direction. Exact LDL checks also establish H²(g=.11) PSD and the116×116 Gram of{basis,H(g=.11)basis} PSD; its rank is87. These are supplementary consistency checks on the physical contractions, not substitutes for them.

All basis vectors remain translation-invariant, even-parity SU(2) singlets because the generating scalar Hamiltonian pieces preserve those symmetries. A future residual-pencil argument must use a cutoff for the full untruncated even-singlet sector, plus separate global-ground identification. This matrix review itself supplies no new spectral endpoint or coupling frontier.

## Resources and reproducibility
The authorized single independent complete pass used at most40.18 measured CPU seconds and54,016KiB peakRSS under500CPU seconds/100MiB onCPU4. Sparse benchmarks predicted227–254 seconds; the full warm cache made the completed pass faster. Physical runtime, compilation, and cached algebra are separately recorded. Exact assembly/rank/PSD checks used about1.08 CPU seconds and16,556KiB under60CPU seconds/256MiB. There was no second full physical replay.

FULL_INPUT_SHA256.json pins the exact full-pass source, executable, geometry, coefficients and producer row/seal. REPRODUCE.sh verifies those inputs and the final review seal, then repeats only the cached exact assembly to fresh outputs. FULL_REPLAY.sh documents a fresh physical replay and requires new explicit authorization; it is never invoked by default. The freshly computed full.json and progress record are sealed as evidence from the one authorized independent pass.
