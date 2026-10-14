# q6 residual-direction fixture and sampled cost

2026-10-10 21:17 EDT / 2026-10-11 01:17 UTC. The producer fixture passed, with independent review pending. This run did not validate the full 8×4 calculation, certify the 58D matrix, search higher couplings or establish a new spectral result.

## Fixture and comparison

Run `REPRODUCE.sh` to compile separately (CPU 3, 512 MiB, 40 CPU seconds) and reproduce the full 4×2 fixture plus strictly partial 8×4 benchmark (CPU 3, 100 MiB, with respective hard caps of 2 and 3 CPU seconds). The executable accepts only `fixture` and `benchmark`. Fixture requires N=8. There is no full 8×4 mode.

The standalone kernel retains accepted matching construction functions in `base_kernel.inc` and initialization in `init_kernel.inc`, copied from the sealed split kernel without modifying it. New generic scalar lookup/actions are in `fixture.cpp`. Inputs are hashed in `INPUT_SHA256.json`. The prior plan and independent-review manifest hashes match the parent's expected identities.

- Physical Hamiltonian: ordinary periodic bilayer H′=Q+gA/2. This fixture tests H200=200Q+11A, so g=.11.
- New vector: T=(C†R)cR+(D6M)cM. Benchmark coefficients are exactly the saved .11 reference in `bilayer_next_residual_direction_plan/cached_shapes.json`, copied to `reference_coefficients.txt`.
- The 4×2 fixture uses cR[j]=j+1 and cM[j]=(-1)^j(j+2), j=0..4, to exercise mixed signs. It has 21 old columns [vacuum,B(5),L(5),R(5),M(5)] plus T. It is not asserted to have rank 22 on that small torus. Prior accepted exact .11 Schur norm establishes rank 58 on 8×4.
- Full 4^8 Cartesian singlet/triplet states are generated independently of matching contractions. Direct bond action checks every amplitude of CT, D6T and KT=(CC†−C†C)T. It independently checks the q8 norm and every new Gram, H200 and H200² cross/self entry against all 21 old basis columns. Q includes every occupied rung, and q8 is explicitly retained in the small physical image.
- The physical fixture has TKT=−2678612736, CT norm=3613305600, q8 norm=934692864. Hence dropping negative commutator terms is detected. Fixture assertion failures abort.

## Generic lookup and all-support coverage

Scalar cache shape is C(31,5)×15×int128 = 40,778,640 bytes. The existing all-q4 R cache is 6,041,280 bytes. Readiness flags add 169,911 bytes. The full scalar array is allocated/zero-initialized even in the benchmark, while only requested entries are populated. Normalize by translating a chosen occupied site to the origin, sort, combinadically rank the other five sites, and permute channels with a complete 720×15 table. Lazy entries are computed by the exact unprojected formula above, not an M-support predicate.

The dispersed 8×4 benchmark visits 16 q4 and 129 q6 supports, fills 8,469 normalized cache entries, performs 12,023 lookups and verifies all six anchor choices for each sampled q6 support (774 equalities). It explicitly encounters 56 supports with T nonzero and all old M columns zero. The small physical fixture checks every 4×2 q6 support and all anchors. Empirical equality over the full 8×4 system remains untested. The transformation rule is also justified by translation-invariant edge weights/orbit classes and matching-channel permutation.

The partial benchmark saves unnormalized sample sums in its G/H/J arrays and norm-labelled fields. Its q4 and q6 samples have different densities. In particular its printed `q8_creation_norm` is not a physical norm and cannot be used in a certificate. `partial:true` labels this output. Only `fixture_4x2.json` contains complete physical values.

## Complete mixed-moment formulas

Let U=1200T+11DT. In sector q4, HT=11CT. Its q6 component is U, and its q8 component is 11C†T. All expressions below are exact inner products in the matching Gram metric, summed over complete supports for the fixture.

- G(T,M)=<T,M>, all other old-sector Gram cross entries zero.
- H200(T,L)=11<CT,L>.
- H200(T,R)=11<CT,R>.
- H200(T,M)=<T,1200M+11DM>.
- H200²(T,B)=121<CT,L>.
- H200²(T,L)=8800<CT,L>+121<CT,R>+11<U,M>.
- H200²(T,R)=8800<CT,R>+121<CT,DR>+11<U,C†R>.
- H200²(T,M)=242<CT,CM>+<U,1200M+11DM>+121<T,KM>.
- H200(T,T)=1200||T||²+11<T,DT>.
- H200²(T,T)=242||CT||²+||U||²+121<T,KT>.

The factor 242 includes both the q4 image and the q8 normal-ordered annihilation contribution. The generic KT contains positive empty-edge terms, negative occupied-edge contractions and both positive empty-center and negative occupied-center ordered wedges. No M-active filtering is applied. GMP is used for every bilinear product and accumulation. The int128 type is used only for scalar amplitudes and checked local additions/products.

## Integer bounds

The tighter bounds in this original section were superseded by [BOUND_ERRATUM.md](BOUND_ERRATUM.md). They are retained here as the historical calculation. The erratum gives the corrected coarse bounds.

Both input coefficient arrays are explicitly asserted to have absolute values at most 2^48. Existing family amplitudes obey their int32 contract. For this degree-four graph one can more tightly bound each matching/orbit L amplitude by 4, M by 24, R by 128, DM by 1152, and C†R by 3840 (bounds intentionally overcount). Thus T is bounded by 14×(3840+1152)×2^48 <2^65. A conservative implementation-independent bound using only int32 family outputs is |T|<2^84.

For a scalar q6 channel bound B, D has at most 24 weighted hopping contributions and at most 24 weighted interaction contributions, so |DT|≤48B. K has ≤192 empty-edge weight, ≤48 occupied-edge contraction weight and ≤288 ordered-wedge weight, hence |KT|≤528B. Even the coarser CT bound 64 edges×15 channels×3 contraction×2 edge multiplicity gives |CT|≤5760B. U is bounded by (1200+11×48)B<2^11 B. These bounds remain below 2^127 starting from B<2^84. Checked arithmetic aborts on violation. GMP avoids any int128 norm-product assumption.

## Cost estimate and incomplete calculations

The final sample's exact resource measurements and scaled projection are in `resources_and_gate.json`. Observed sample variation gave roughly 134–158 CPU seconds for a linear full-support estimate. A two-times planning margin is about 317 CPU seconds at the final measurement. This estimate comes from samples and is not a rigorous runtime bound. Dense supports and GMP growth may change it. Peak resident memory is about 47 MiB with the full scalar allocation present, below 100 MiB.

The proposal is a separate 360 CPU-second hard cap with 100 MiB, or a tighter 180-second cap with resumable execution and possible interruption. This recommendation does not authorize either run. The current executable is fixture-only/sample-only. Any production implementation must checkpoint additive blocks before enabling a full mode.

The missing calculations are all full 8×4 q4/q6 CT/DT/K mixed and self contractions, exact N/q translation normalization, complete 58×58 assembly, independent review and subsequent resource authorization. No complete production block was claimed from the sample. No projected H² was substituted. Repository-wide status updates were handled separately from this fixture.
