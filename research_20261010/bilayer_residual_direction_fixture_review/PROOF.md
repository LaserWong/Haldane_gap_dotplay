# Independent residual-direction fixture review

## Verdict and scope
PASS for the complete 4×2 physical fixture and the sampled 8×4 lookup/kernel gate. This is neither a complete 8×4 matrix certificate nor a new ground or gap bound. The producer original seal and its separately sealed amplitude-bound erratum are verified. Every input hash is checked against the accepted source, including geometry and the cached residual-shape provenance.

## Independent physical construction
The reviewer uses the accepted Cartesian rung basis and directly checks its 16×16 edge operator against the physical spin-half Hamiltonian. On all 4^8 states of the periodic weighted 4×2 graph, independently form B, L=C†B, R=D L, M=C†L and T=Σ(j+1)C†R_j+Σ(-1)^j(j+2)D M_j. Sparse physical actions have no matching-channel implementation in common with the producer kernel. Every state amplitude of T, CT, DT and KT is checked, K=[C,C†]. All 22 entries in each new G, H200 and H200² row match independent direct physical contractions. TKT is negative, while ||C†T||²=||CT||²+<T,KT> is positive: dropping the negative commutator contributions would fail.

H200T has q4 component11CT, q6 component U=1200T+11DT and q8 component11C†T. Thus its complete squared norm is ||U||²+242||CT||²+121<T,KT>. Mixed rows follow by matching sectors. For L they are 8800<CT,L>+121<CT,R>+11<U,M>; for R, 8800<CT,R>+121<CT,D R>+11<U,C†R>; for M, 242<CT,CM>+<U,1200M+11DM>+121<T,KM>. B has121<CT,L>, vacuum zero. These identities retain all oriented cross terms and the signed q8 contribution.

Every old column has definite occupation q_j and T has occupation6. Set A_j=(H200_j−1200G_j)/11 and A²_j=(J200_j−1440000G_j−2200(6+q_j)A_j)/121. Then H(g)_j=6G_j+(g/2)A_j and H²(g)_j=36G_j+(g/2)(6+q_j)A_j+(g²/4)A²_j. Direct independent A and A² contractions verify these complete polynomial identities. No projected-H² substitution is used.

## Global cache and sample
All169911 fixed-origin q6 subsets have distinct combinadic ranks filling the entire cache range. All720 permutations and15 perfect matchings give invertible, orientation-correct relabelings. Translation equivariance follows because orbit B and the periodic C†,D operators commute with translations; T does too. The instrumented producer copy additionally compares cached T to uncached rawT at every sampled support and compares all six translation anchors. The129 sampled supports give774 anchor checks, including56 supports with nonzero T and all M channels zero. All deterministic sample quantities equal the frozen producer. There is no M-active restriction in generic lookup.

## Integer safety
The corrected bound, not the narrower initial README estimate, is used. The28 coefficients have magnitude≤2^48. Source channels are checked signed32-bit values. The safe bound |T|<B=2^84 exceeds28·2^31·2^48. Neighbor/channel counts give |DT|≤924B, |KT|≤20172B, |CT|≤5760B and |U|≤11364B, all below signed128 capacity. Checked scalar arithmetic catches overflow. Inner products convert each amplitude to GMP before multiplication; large norms are not accumulated in fixed-width integers. The small weighted graph obeys the same conservative bounds.

## Cost and production prerequisites
The frozen sample allocates the full40,778,640-byte scalar cache and6,041,280-byte R cache, with measured peak47,872KiB. Final producer phase timings project158.36 CPU seconds for all fixed-origin supports; twice that is316.71, superseding the earlier134/270 estimate. The reviewer instrumented sample includes extra uncached evaluations and is slower. Neither extrapolation is a guarantee; support-dependent lookup/GMP costs and timing noise remain. Memory is credible because full caches were allocated. A separately authorized checkpointed cap is needed for a complete pass.

The frozen sample is partial and unnormalized. Full export MUST keep q4 and q6 contributions separate, multiply by N and exactly divide by4 or6 respectively, then add them. In particular8×4 uses8 and16/3, so scaling an already combined row is wrong. Production must reject incomplete/overlapping coverage, bind source, binary, geometry and coefficients, and charge interrupted work to the budget. The separate production gate is outside this fixture acceptance. No full8×4 pass was run for this review.

## Reproduction
REPRODUCE.sh verifies this manifest, freshly compiles the instrumented copy on CPU4 under512MiB, and repeats small/sample runs and independent Cartesian contractions under100MiB. Outputs go to check/ and are compared after dropping runtime-only fields. The instrumentation adds only vector export and uncached T comparisons; frozen producer files remain unchanged. Runtime and compilation measurements are saved separately.
