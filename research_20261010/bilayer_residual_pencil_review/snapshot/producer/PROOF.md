# Shared complete second-moment matrix fixture and benchmark

Producer fixtures pass; independent review pending. No full8x4 matrix is claimed.

The current basis B,L,U=R+M has16 columns on4x4 and43 on8x4. The implementation changes only the output contraction: accepted matching-coordinate local actions generate d-column P,CM,T and commutator amplitudes, then exact matrix bilinears are accumulated. It does not introduce R/M search freedom.

All fixed-origin q4 and q6 supports are traversed for a full run, including supports with zero M. M-active filtering is applied only to the commutator bra. The identity ||C†M||²=||CM||²+<M,[C,C†]M> is retained with its exact signed hard-core commutator. Translation weights are N/4 for q4 and N/6 for q6. No q8 state is built.

The emitted PP,TT,CMCM,COMM blocks reconstruct the complete U,U second moment using the formula in ../bilayer_residual_pencil_plan/PLAN.md. The q2 piece D2=S*Gpair^-1 S uses the complete invariant pair basis. H(B,L) lies exactly in(B,L,U), so J_(B,L),all=Hmap* K supplies every mixed block from the cached first moment. The cached old J0 is reproduced exactly. In particular this is not a projected square of the enlarged K matrix.

The4x2 and4x4 full runs agree exactly with all four separately saved scalar quadratic forms. On4x4 the assembled complete H² expectation also agrees with the independently accepted physical second moment for the saved16D trial. Exact PSD checks pass for PP,TT,CMCM,completeq8 and completeJ. The signed COMM need not be PSD. The complete coupling-independent Q²,(QA+AQ)/2,A²/4 matrices are saved for both fixtures; their polynomial identity is checked at a physical coupling distinct from coefficient-extraction points. The formal extraction points g=±1 are algebra only, with no stability inference.

Arithmetic guards: local amplitude updates use checked int32 additions, inherited from the accepted engine; each contraction product is evaluated in signed int128. Two int32 entries and a matching-Gram factor<=27 give magnitude below2^67, safely inside int128. Every accumulator addition is checked for overflow. A coarse bound using at most C(63,5)<2^23 supports,225 matching pairs, factor27 and int32 entries stays below2^100; the translation rescaling N<=64 stays below2^106. Actual authorized runs are much smaller. Matrix commutator asymmetry would fail the exact assembly checker.

Measured CPU3 kernel times:4x2 .000581319s,4x4 .0946979s,8x4 sample .164066s. The sample visits2248/4495 q4 and2023/169911 q6 supports with a deterministic stride. All cache construction is included. Phase-scaled full8x4 estimate is4.1790745153s and peak RSS7680KiB. Sampling is NOT a certificate and cannot prove full-run timing; proposed future gate40CPU seconds/100MiB provides substantial headroom. Full8x4 remains unlaunched.

For later endpoint optimization, c*(J−(a+ell)K+a ell G)c<0 with ell<a proves E0>ell provided the full untruncated applicable sector has at most one eigenvalue below a. Here a=r2 is valid only in the even-singlet sector after the exact odd-sector counting argument; r1 is the global first-excited comparison used separately for unique-ground identification. Every basis vector is an exact even singlet, so rational coefficient rounding preserves its sector. No residual-pencil energy optimization is performed in this fixture package.
