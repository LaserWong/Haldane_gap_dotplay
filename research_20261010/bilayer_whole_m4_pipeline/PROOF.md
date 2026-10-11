# Algebra, convention and safety

Cartesian rung states have a scalar vacuum and three real triplet colors. C† creates a δ-paired triplet pair; C annihilates it; D hops an occupied triplet or acts on two occupied sites by permutation minus singlet contraction. Direct composition matches occupation masks and joins pairings with union-find. Every closed color loop contributes exactly 3. General qi→qo contractions include untouched spectator lines. The source matching basis is lexicographically generated perfect matchings, with sizes 1,1,3,15 for q=0,2,4,6. Its Gram entry is 3 to the number of loops in the superposed matchings.

The distinct-pair probe for a given matching assigns a distinct Cartesian color to each of its q/2 pairs. Any other matching joins at least two different colors and vanishes. The selected matching evaluates to one. Thus these probes extract coefficients exactly for q≤6 using at most three colors, and prove linear independence. The method is not asserted for q≥8. All 24 q4 and 720 q6 relabelings on a selected support are compared with physical χ; every occupied anchor is checked for χ6 and v on every small invariant q6 target.

Let m=ψ6, cm=Cm, ed=E†m, x=C†cm, γ=x+Km, χ=Tψ. Then χ8=11C†m and z10=121(C†)²m. v=4400m+22χ6−121C†ψ4=17600m+11χ6+121Dm. The two v forms agree in every complete fixture target. The implementation uses q≤6 data only.

The fifteen exact signed quantities, in code order, are:
1. 2<x,Dm>; 2. −<cm,Dcm>; 3. <Km,Dm>; 4. <m,Nm>;
5. ||Cv||²; 6. <v,Kv>; 7. 242<v,Ecm>; 8. 242<v,Nm>;
9. 14641||ed||²; 10. 14641<m,Fm>;
11. ||γ||²; 12. 2<x,Km>; 13. −<cm,Kcm>; 14. ||Km||²; 15. <m,Lm>.
Their physical reference retains C on the right where appropriate, e.g. term1=2<cm,CDm>, so those adjoint rearrangements are independently checked. N=[C,[D,C†]] is oriented and is not replaced by N†. F=[E†,E], L=[[C,K],C†]. The first four sum to d8=<C†m,D C†m>. Terms5–10 sum to ||z8||²; 14641 times terms11–15 is ||z10||².

n8=||cm||²+<m,Km>. m2=||χ≤6||²+121n8. m3 comprises the exact q≤6 diagonal/adjacent-sector expression plus 193600n8+1331d8+242<χ6,γ>. zq=200qχq+11Dχq+11C†χ(q−2)+11Cχ(q+2); at q6 the final term is replaced by121γ. m4=Σ(q≤6)||zq||²+Σ(terms5–10)+14641Σ(terms11–15). Complete fixture comparisons use direct physical T²ψ, including q8/q10 when present.

Translation: sum over all supports equals N/q times sum over supports containing the origin for any invariant scalar density. Count pairs (support, occupied site) and translate that site to the origin; this proof does not require free translation orbits and includes stabilizers. The small invariant fixtures check this equality exactly for all22 accumulator components, separately collecting each sector. The inherited compiled rules already include exact anchored canonicalization/stabilizer coefficients and every physical embedding; do not divide their action by32 again. At production q4 andq6 final density weights are8 and16/3, not32. The bounded sample deliberately does not normalize its mixed sampled sectors.

Mutation assertions detect N→N†, deletion of the negative term13, removal of the combined q8 cross, conflation of cR/cM, and filtering z6/Kv to m-active targets. Localized fixtures explicitly require m-zero targets with nonzero z6 and Kv. Successful8×4 samples contain285 m-zero q6 targets,281 with nonzero z6 and275 with nonzero Kv.

## Integer bounds

A conservative physical l1 bound uses witness coefficients <2^48, orbit-pair source l1<2^59, and each elementary operator C,C†,D l1 norm<2^8. Therefore ψ and every individual source sector have l1<2^77; T has l1 norm<2^14. χ<2^91 and z<2^105. The scalar-channel coefficients are exact physical probes and obey these bounds. The needed auxiliary images have conservative bounds: m<2^77; cm,Dm<2^85; K m and E†m<2^94; x<2^93; γ<2^95; N m<2^103; Fm,Lm<2^112; v<2^97; Cv<2^105; Kv<2^114; Ecm<2^102; Dcm<2^93; Kcm<2^102; Dχ6<2^99. These fit signed int128. This table bounds final source/image coefficients; potentially canceling partial accumulations additionally use checked int128 adds/products and abort on overflow rather than assuming the final bound suffices.

Every scalar bilinear, coefficient scaling and moment accumulation is GMP. int128 import uses signed two-word mpz_import, not narrowing to long. Sample maximum reported bilinear/input GMP limb count is2; this is not a maximum final-accumulator limb claim. Analytic source elementary products are safely bounded by the same small source coefficients and edge weights. The code retains assertions: do not compile with NDEBUG.
