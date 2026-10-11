#Next bounded ground-lower route after57D splitting

Planning and cached exact algebra only. No new support contraction or local-operator experiment is launched.

##Recommendation and what is actually missing

Stop coefficient tuning in the existing families. Compare two staged routes:

A. Add ONE q6 projected-residual shape Tpsi=(C†R)cR+(D6M)cM to the accepted57D basis, giving58D. It preserves maximum trialq6 and uses only the already proved hard-core commutator K=[C,C†] for q8 norms. A q4 companion Ppsi=(D4R)cR+(CM)cM would give59D, but its new orthogonal component is much smaller; defer it initially.

B. Use the two-vector Krylov trial {psi,H'psi} built from the optimized exact57D psi. It includesq8, targets the dominant missing residual directly, and needs exact moments m3=<H'^3> and m4=<H'^4>. Start with m3 plus a rigorous inexpensive upper onm4. Only if that bound is inadequate should one implement the higher nested commutators for exactm4 withoutq10 enumeration.

The resource-controlled first scientific choice is to derive/fixture the normal-order m3 identity before committing to a costly full support pass. In parallel, the58D T-only implementation is the simpler physical residual extension because it needs no new commutator theorem. Neither route is currently known sufficient for the selected .11 target.

##Cached exact rank and residual geometry

cached_shapes.json derives exact positive Schur norms of Ppsi outside span(L,R) and Tpsi outside span(M), using only accepted split matrices. Thus57+Tpsi has rank58, and57+Ppsi+Tpsi has rank59 at both .11/.12. No numerical rank threshold is used.

For the .11 endpoint witness, fractions of its complete variance are:

- q4 outside the57D space: .0003013701 (0.0301%).
- q6 outside the57D space: .0169119085 (1.6912%).
- q8 outside the space: .6142634989 (61.4263%).
- residual remaining inside the57D space: .3685232225.

At .12 the corresponding fractions are .0002964243,.0172462238,.6094694087,.3729879432. They sum exactly to the complete variance before decimal display. Tpsi may help cancel a q8 image despite its modest norm, but this is a possibility, not a certificate. Ppsi has less direct promise. The q8-dominant component motivates the true Krylov alternative.

##Route A:58D T-only complete residual

Use the UNPROJECTED integer Tpsi as the additional basis vector; its span with57D equals that of its rationally orthogonalized version. This avoids large-denominator physical coefficients and preserves exact singlet/even symmetry.

The Gram norm and all first-H cross entries with existing57D are already determined by accepted image blocks; the NEW self first-H entry contains <Tpsi,D6Tpsi> and must be physically contracted. Full-H² new cross/self entries require:

- CTpsi onq4,
- D6Tpsi onq6,
- q8 cross Gram between C†M_i and C†Tpsi, and the Tpsi q8 norm.

The q8 identities are exact:

 <C†u,C†v>=<Cu,Cv>+<u,Kv>, for u,v inq6.

Thus old-M/new-T cross terms use CM_i,CTpsi and M_i*K Tpsi; the new norm uses ||CTpsi||²+<Tpsi,K Tpsi>. All q4/q6 image cross terms with old columns must also be included. Neither a projected H² nor a scalar variance of one old vector supplies the new full58D matrix.

The commutator theorem already applies to arbitraryq6 vectors, but the current implementation's Mval-specific lookup does NOT. Implement a generic translation-equivariant Tpsi lookup, and independently test the entire signed K action on small geometries. Never substitute M-active supports: Tpsi and K Tpsi are nonzero outside them.

Optional59D Ppsi additionally needs CPpsi(q2),D4Ppsi(q4),C†Ppsi(q6), new first-H diagonals/cross with Tpsi, and all resulting second-moment cross entries. It does not createq8 by itself.

##Route A memory/time plan

Same169911 fixed-originq6 and4495 fixed-originq4 supports; no newq8 enumeration. A translation-normalized scalar Tpsi cache can use169911*15*16=40778640 bytes with signedint128 amplitudes. The existing R-family cache uses6041280 bytes. An optional fullq4 Ppsi cache uses35960*3*16=1726080 bytes. Working data should fit100MiB if exact accumulation is streamed; this is an implementation estimate that requires measurement.

For a genericq6 lookup, translate any occupied site to the origin, sort, and permute matching channels. The cache must give the same exact amplitudes for every choice of translated occupied site. Fixture this invariance before production. A precomputed720-permutation by15-matching table is only10800 entries and avoids repeated matching searches. Coefficient-amplitude bounds must be checked: a dot product of14 int32 source amplitudes with <=2^48 coefficients lies below2^83; subsequent local sums remain withinint128 only after a new explicit bound. Norm products can exceedint128 and must use GMP, as in the accepted scalar engine.

The source-cache build is comparable to one currentq6 pass, but generic K lookup and GMP new-vector bilinears can dominate. A tentative planning range is20–120CPU seconds, not a measured promise. Proposed gate: local fixture plus cache/sampled-action benchmark<=5CPU seconds/100MiB; only then consider one full pass with a conservatively projected cap up to180CPU seconds/100MiB. No such action is authorized by this plan. A failed memory/projection gate should stop, not fall back to a full physical-state cache.

##Route B exact two-vector moment requirements

Normalize psi to1 and write chi=H'psi. Then

 G2=[[1,m1],[m1,m2]], K2=[[m1,m2],[m2,m3]], J2=[[m2,m3],[m3,m4]].

m0,m1,m2 are already certified from the full57D matrix. Exactm3 is enough for the new first moment. A sufficient upper matrix for the complete second moment is obtained by replacing onlym4 by a rigorous upper M4. With a verified global lower ell0 and the elementary physical upper U=N(1+g), spectral calculus gives

 H'^2(H'−ell0)(U−H')>=0,
 m4 <= (U+ell0)m3−ell0*U*m2 = M4.

This uses the actual verified lower ell0, not a hypothetical target. It is valid even when the ground energy is negative. Replacingm4 byM4 makes J2 larger in Loewner order, so a negative Temple pencil with that upper J2 is still a valid physical lower-endpoint witness. If this bound is too loose, save the shortfall before implementing exactm4. The bound may be very loose because U=35.52 atg=.11; no success is assumed.

This is a TWO-dimensional Krylov search, not an immediate58D augmentation of the whole57D basis. Augmenting all57D bychi also needs the full vector of cross third moments <phi_i,H'^3psi>, not merely the scalar m3. Do not claim the2D data supplies that larger matrix.

##Normal ordering that avoidsq8/q10 state enumeration

Let A=C+C†+D, K=[C,C†], E=[D,C†], and let m=M cM be the q6 component ofpsi. Here D acts within each occupation sector. For t=g/2, chi8=t C†m. All operators below are the exact hard-core operators, not canonical bosons.

The newq8 contribution to m3 contains <C†m,D C†m>. An exact normal-ordered identity is

 <C†m,D C†m>
 =2Re<CM,C Dm>−<CM,D4 CM>+<Km,Dm>+<m,[C,[D,C†]]m>.

All expectations useq4/q6 vectors. The last nested commutator contains connected triples of local edges, with support at most4rungs. Intermediate terms need not be individually Hermitian; retain their orientations and verify the complete real identity independently. The lower sectors andq6↔q8 coupling use C C†m=C†Cm+Km and are also computed onq<=6. This is the exact missingm3 physical input.

For exactm4, theq0..6 components ofH'chi can be streamed using that same C C† identity. Itsq8 component is

 (H'chi)8 = C†v+t²E m,
 v=8t m+t chi6+t²D6m,

and itsq10 component is t²(C†)²m. Then

 ||C†v+t²E m||²
 =||Cv||²+<v,Kv>+2t²Re<v,C E m>
   +t⁴[||E†m||²+<m,[E†,E]m>],
 C E m=E C m+[C,E]m.

For theq10 norm, define L=[[C,K],C†]. The exact identity is

 ||(C†)²m||²
 =||C†Cm+Km||²
   +2Re<CM,C K m>−<CM,K4 CM>+||Km||²+<m,Lm>.

Thus no q10 output needs to be constructed. The new obligations are generic K onq6 vectors plus the connected local operators [C,E], [E†,E] andL. The last two contain up to4local edges and up to5rungs. Their exact signed hard-core action must be derived and independently fixture-tested; the currently accepted K proof alone does not certify them.

##Route B resource gate and comparison

Directq8 enumeration would requireC(31,7)=2629575 fixed-origin supports with105 matchings; directq10 would requireC(31,9)=20160075 supports with945 matchings. A scalarint128q8 cache alone is4417686000 bytes. These paths are outside the present resource envelope and are not proposed.

On the8x4 degree4 graph, a coarse connected ordered-edge-tuple count is64*7*12=5376 triples and64*7*12*16=86016 quadruples before algebraic cancellation; translation normalization reduces those counts by32 only after invariance is proved. They are operation-count ceilings for local motif generation, not runtime estimates for the full expectation. Spin-channel expansion and matching contractions can multiply cost substantially. A naive per-q6-support scan of every motif is not an acceptable implementation plan.

Propose first a proof/fixture stage for the triple-edge m3 operator on at most4rungs (local Hilbert dimension<=256), with sparse exact local actions, motif canonicalization and checkpointed term counts. It needs no full-system ED or large support pass. After measuring the reduced motif count and lookup work, make a new support-time/memory proposal. Exactm4's four-edge/five-rung operators (local Hilbert dimension<=1024) should be a separate stage only if the rigorousM4 upper fails by an actionable amount. No defensible fullm4 runtime promise exists yet.

All endpoint applications still require the full untruncated even-sector second-level lower a=r2, exact odd counting, and separate globalr1 unique-ground identification. All physical lower claims and any all-size scalar consequence require independent review. These algebraic routes preserve even singlet symmetry under H',C,C†,D and occupation projection.
