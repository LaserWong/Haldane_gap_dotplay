# Next bounded ground-lower route after 57-dimensional splitting

Planning and cached exact algebra only. No new support contraction or local-operator experiment is launched.

## Proposed calculations and missing inputs

Stop coefficient tuning in the existing families. Compare two staged routes:

A. Add one q6 projected-residual shape Tpsi=(C†R)cR+(D6M)cM to the accepted 57-dimensional basis, giving a 58-dimensional basis. It preserves maximum trial q6 and uses only the already proved hard-core commutator K=[C,C†] for q8 norms. A q4 companion Ppsi=(D4R)cR+(CM)cM would give a 59-dimensional basis, but its new orthogonal component is much smaller. Defer it initially.

B. Use the two-vector Krylov trial {psi,H'psi} built from the optimized exact 57-dimensional psi. It includes q8, targets the dominant missing residual directly, and needs exact moments m3=<H'^3> and m4=<H'^4>. Start with m3 plus a rigorous inexpensive upper bound on m4. Only if that bound is inadequate should one implement the higher nested commutators for exact m4 without q10 enumeration.

The resource-controlled first scientific choice is to derive the normal-order m3 identity and test it on small exact systems before committing to a costly full support pass. In parallel, the 58-dimensional T-only implementation is the simpler physical residual extension because it needs no new commutator theorem. Neither route is currently known sufficient for the selected .11 target.

## Cached exact rank and residual geometry

cached_shapes.json derives exact positive Schur norms of Ppsi outside span(L,R) and Tpsi outside span(M), using only accepted split matrices. Thus 57+Tpsi has rank 58, and 57+Ppsi+Tpsi has rank 59 at both .11/.12. No numerical rank threshold is used.

For the .11 endpoint witness, fractions of its complete variance are:

- q4 outside the 57-dimensional space: .0003013701 (0.0301%).
- q6 outside the 57-dimensional space: .0169119085 (1.6912%).
- q8 outside the space: .6142634989 (61.4263%).
- residual remaining inside the 57-dimensional space: .3685232225.

At .12 the corresponding fractions are .0002964243,.0172462238,.6094694087,.3729879432. They sum exactly to the complete variance before decimal display. Tpsi may help cancel a q8 image despite its modest norm, but this is a possibility, not a certificate. Ppsi has less direct promise. The q8-dominant component motivates the true Krylov alternative.

## Route A:58-dimensional T-only complete residual

Use the UNPROJECTED integer Tpsi as the additional basis vector. Its span with the 57-dimensional basis equals that of its rationally orthogonalized version. This avoids large-denominator physical coefficients and preserves exact singlet/even symmetry.

The Gram norm and all first-H cross entries with the existing 57-dimensional basis are already determined by accepted image blocks. The new self first-H entry contains <Tpsi,D6Tpsi> and must be physically contracted. Full-H² new cross/self entries require:

- CTpsi on q4,
- D6Tpsi on q6,
- q8 cross Gram between C†M_i and C†Tpsi, and the Tpsi q8 norm.

The q8 identities are exact:

 <C†u,C†v>=<Cu,Cv>+<u,Kv>, for u,v in q6.

Thus old-M/new-T cross terms use CM_i,CTpsi and M_i*K Tpsi. The new norm uses ||CTpsi||²+<Tpsi,K Tpsi>. All q4/q6 image cross terms with old columns must also be included. Neither a projected H² nor a scalar variance of one old vector supplies the new full 58-dimensional matrix.

The commutator theorem already applies to arbitrary q6 vectors, but the current implementation's Mval-specific lookup does NOT. Implement a generic translation-equivariant Tpsi lookup, and independently test the entire signed K action on small geometries. Never substitute M-active supports: Tpsi and K Tpsi are nonzero outside them.

Optional 59-dimensional Ppsi additionally needs CPpsi(q2),D4Ppsi(q4),C†Ppsi(q6), new first-H diagonals/cross with Tpsi, and all resulting second-moment cross entries. It does not create q8 by itself.

## Memory and time estimates for Route A

Same 169911 fixed-origin q6 and 4495 fixed-origin q4 supports. No new q8 enumeration. A translation-normalized scalar Tpsi cache can use 169911*15*16=40778640 bytes with signed int128 amplitudes. The existing R-family cache uses 6041280 bytes. An optional full q4 Ppsi cache uses 35960*3*16=1726080 bytes. Working data should fit 100 MiB if exact accumulation is streamed. This is an implementation estimate that requires measurement.

For a generic q6 lookup, translate any occupied site to the origin, sort, and permute matching channels. The cache must give the same exact amplitudes for every choice of translated occupied site. Fixture this invariance before production. A precomputed 720-permutation by 15-matching table is only 10800 entries and avoids repeated matching searches. Coefficient-amplitude bounds must be checked: a dot product of 14 int32 source amplitudes with <=2^48 coefficients lies below 2^83. Subsequent local sums remain within int128 only after a new explicit bound. Norm products can exceed int128 and must use GMP, as in the accepted scalar engine.

The source-cache build is comparable to one current q6 pass, but generic K lookup and GMP new-vector bilinears can dominate. A tentative planning range is 20–120 CPU seconds, not a measured promise. Proposed gate: local fixture plus cache/sampled-action benchmark<=5 CPU seconds/100 MiB. Only then consider one full pass with a conservatively projected cap up to 180 CPU seconds/100 MiB. No such action is authorized by this plan. A failed memory/projection gate should stop, not fall back to a full physical-state cache.

## Exact two-vector moments for Route B

Normalize psi to 1 and write chi=H'psi. Then

 G2=[[1,m1],[m1,m2]], K2=[[m1,m2],[m2,m3]], J2=[[m2,m3],[m3,m4]].

m0,m1,m2 are already certified from the full 57-dimensional matrix. Exact m3 is enough for the new first moment. A sufficient upper matrix for the complete second moment is obtained by replacing only m4 by a rigorous upper M4. With a verified global lower ell0 and the elementary physical upper U=N(1+g), spectral calculus gives

 H'^2(H'−ell0)(U−H')>=0,
 m4 <= (U+ell0)m3−ell0*U*m2 = M4.

This uses the actual verified lower ell0, not a hypothetical target. It is valid even when the ground energy is negative. Replacing m4 by M4 makes J2 larger in Loewner order, so a negative Temple pencil with that upper J2 is still a valid physical lower-endpoint witness. If this bound is too loose, save the shortfall before implementing exact m4. The bound may be very loose because U=35.52 at g=.11. No success is assumed.

This is a two-dimensional Krylov search, not an immediate 58-dimensional augmentation of the whole 57-dimensional basis. Augmenting the entire 57-dimensional basis by chi also needs the full vector of cross third moments <phi_i,H'^3psi>, not merely the scalar m3. Do not claim the 2-dimensional data supplies that larger matrix.

## Normal ordering that avoids q8/q10 state enumeration

Let A=C+C†+D, K=[C,C†], E=[D,C†], and let m=M cM be the q6 component of psi. Here D acts within each occupation sector. For t=g/2, chi8=t C†m. All operators below are the exact hard-core operators, not canonical bosons.

The new q8 contribution to m3 contains <C†m,D C†m>. An exact normal-ordered identity is

 <C†m,D C†m> =2Re<CM,C Dm>−<CM,D4 CM>+<Km,Dm>+<m,[C,[D,C†]]m>.

All expectations use q4/q6 vectors. The last nested commutator contains connected triples of local edges, with support at most 4 rungs. Intermediate terms need not be individually Hermitian. Retain their orientations and verify the complete real identity independently. The lower sectors and q6↔q8 coupling use C C†m=C†Cm+Km and are also computed on q<=6. This is the exact missing m3 physical input.

For exact m4, the q0..6 components of H'chi can be streamed using that same C C† identity. Its q8 component is

 (H'chi)8 = C†v+t²E m,
 v=8t m+t chi6+t²D6m,

and its q10 component is t²(C†)²m. Then

 ||C†v+t²E m||² =||Cv||²+<v,Kv>+2t²Re<v,C E m> +t⁴[||E†m||²+<m,[E†,E]m>], C E m=E C m+[C,E]m.

For the q10 norm, define L=[[C,K],C†]. The exact identity is

 ||(C†)²m||² =||C†Cm+Km||² +2Re<CM,C K m>−<CM,K4 CM>+||Km||²+<m,Lm>.

Thus no q10 output needs to be constructed. The new obligations are generic K on q6 vectors plus the connected local operators [C,E], [E†,E] and L. The last two contain up to 4 local edges and up to 5 rungs. Their exact signed hard-core action must be derived and independently fixture-tested. The currently accepted K proof alone does not certify them.

## Resource limits and alternatives for Route B

Direct q8 enumeration would require C(31,7)=2629575 fixed-origin supports with 105 matchings. Direct q10 would require C(31,9)=20160075 supports with 945 matchings. A scalar int128 q8 cache alone is 4417686000 bytes. These paths are outside the present resource envelope and are not proposed.

On the 8x4 degree 4 graph, a coarse connected ordered-edge-tuple count is 64*7*12=5376 triples and 64*7*12*16=86016 quadruples before algebraic cancellation. Translation normalization reduces those counts by 32 only after invariance is proved. They are operation-count ceilings for local motif generation, not runtime estimates for the full expectation. Spin-channel expansion and matching contractions can multiply cost substantially. A naive per-q6-support scan of every motif is not an acceptable implementation plan.

Propose first a proof/fixture stage for the triple-edge m3 operator on at most 4 rungs (local Hilbert dimension<=256), with sparse exact local actions, motif canonicalization and checkpointed term counts. It needs no full-system ED or large support pass. After measuring the reduced motif count and lookup work, make a new support-time/memory proposal. Exact m4's four-edge/five-rung operators (local Hilbert dimension<=1024) should be a separate stage only if the rigorous M4 upper fails by an actionable amount. No defensible full m4 runtime promise exists yet.

All endpoint applications still require the full untruncated even-sector second-level lower a=r2, exact odd counting, and separate global r1 unique-ground identification. All physical lower claims and any all-size scalar consequence require independent review. These algebraic routes preserve even singlet symmetry under H',C,C†,D and occupation projection.
