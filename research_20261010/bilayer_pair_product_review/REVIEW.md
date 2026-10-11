# Independent bounded review: nearest-neighbor hard-core pair product

2026-10-10 21:10 EDT / 2026-10-11 01:10 UTC.

## Verdict and scope

PASS for the exact fixed-parameter residual obstruction and the analytic normalization argument in the frozen producer assessment. PASS for the stated contraction dimensions as formal representations/cost warnings; no implementation, reachable-state count, wall-time estimate, or feasibility certificate is accepted from them. The proposed range-two and marked corrections are untested plans. No physical full 8×4 vector, eigensolver, norm contraction, H² contraction, endpoint, or gap computation was run.

Producer manifest SHA-256: e3f834e77066581017a7e3e9cedfe1fa6f995bbee4d01d7ef18383f56d441083. All five artifact hashes and all five listed input hashes were verified independently. This review does not modify the producer freeze. The working directory has no accessible Git metadata; no branch/commit status or remote update is asserted.

## Independent local normalization and signs

Use the orthonormal Cartesian rung basis s=(ud−du)/√2, tx=(dd−uu)/√2, ty=i(uu+dd)/√2, tz=(ud+du)/√2. The independently spin-derived matrices obey R^a=|s><ta|+|ta><s|, T=S1+S2, and A_ij=T_i·T_j+R_i·R_j=2(S_i1·S_j1+S_i2·S_j2). Hence H′=Q+(g/2)A. Pair creation takes ss to Ω=Σ_a ta ta, of norm squared 3. Hopping takes ta s to s ta with coefficient +1, and T_i·T_j Ω=−2Ω. The exact 16-dimensional local checks use SymPy, not a producer module. Cartesian complex phases do not introduce pair orientation signs.

The order-g ground-state equation gives 2z+g/2=0, so z=−g/4. The matching expansion has coefficient z^k, without k! or √3: k! disjoint creator orderings cancel the exponential factorial, and overlapping creators vanish.

## Exact uncancellable sector

Every NN edge of the periodic 8×4 graph joins the two checkerboard sublattices. Every matching in ψ=exp(z C†)|0> consequently has equal occupied A and B counts. Let P select q=2 configurations with both occupied sites on one sublattice. Then Pψ=0, so P(Q−rho)ψ=0 for every scalar rho. A pair creation acting on ψ0 produces AB. A pair annihilation acting on ψ4 removes one A and one B from two of each, leaving AB. The occupation-preserving T·T part cannot turn an occupied AB pair into a same-sublattice pair. H′ changes triplet number by at most two, so sectors q≥6 cannot contribute. These exhaust the potential cancellations.

Only hopping on ψ2=z C†|0> survives. For each common neighbor k of u,v there are two initial NN pairs, (u,k) and (v,k); hopping the endpoint k gives Ω_uv in each case. Thus

    P_uv (H′−rho)ψ = g z n_uv Ω_uv,
    n_uv = Σ_k w_uk w_kv.

Distinct occupied supports are orthogonal even when the pairs share one site. Therefore this component of the normalized squared residual is EXACTLY 3g²z² Σ_uv n_uv²/Z; the full squared residual is at least this quantity. For rho equal to the Rayleigh quotient this is a variance lower bound. It is not a claim that all omitted sectors have been computed.

Our independent unordered-pair geometry counts give 32 supports with n=1 and 80 with n=2, Σn²=352. A separate direct enumeration of all NN-pair endpoint hops yields multiplicity 2n for every support. Exhaustive geometry checks of possible q4 NN-pair removals confirm the remaining pair is AB; these are occupancy checks, not a four-triplet physical-state production. The exact coefficient is 1056.

## Norm bound, including doubled loops and periodic seams

For k dimers on a common occupied support, the union of a bra and ket matching has alternating closed components. A coincident pair is a doubled-edge component and contributes 3, exactly like a longer even component. Each vertex has degree two in this union, counting the two copies. There are at most k components, so the overlap is at most 3^k. The same fact follows from Cauchy–Schwarz and ||Ω_M||²=3^k; it does not need planarity or a contractible-loop assumption. Noncontractible torus loops introduce no additional weight or sign.

For the simple 8×4 graph, select the k occupied A sites in binomial(16,k) ways. Each matching has at most 4^k neighbor assignments; an ordered pair of matchings has at most 4^(2k). Requiring injective B assignments and identical bra/ket B support only reduces the count. All contributions at fixed k have the nonnegative factor |z|^(2k). Therefore

    Z ≤ Σ_k binomial(16,k) 3^k 4^(2k)|z|^(2k)
      = (1+48|z|²)^16.

For aggregated positive parallel bonds the weighted degree, rather than the number of neighbors, supplies the same bound; parallel occurrences are never independently occupiable. The producer's weighted-matching proof is equivalent. Arbitrary signed unequal edge amplitudes require a separate absolute-value bound; positivity must not be assumed there.

At g=11/100, z=−11/400 the exact rational result in RESULTS.json is

    variance ≥ 0.00546193724126837… .

For z=−g/4+O(g²), the leading missing contribution is 66g⁴+O(g⁵). This does not exclude all z, any globally optimized one-parameter family, or a dressed state. It produces no energy lower endpoint, uniqueness certificate, or all-size gap.

## Cost and dressing review

The NN PEPS edge dimension 4 gives double-layer edge dimension 16 and width-four column transfer dimension 16^4=65,536. Dense storage of its 2^32 binary64 entries is 32 GiB. The periodic norm is trace(T^8); a single propagated boundary vector is insufficient. Telephone-number partial-pairing counts include arbitrary pairing patterns and unused endpoints, hence are loose ceilings rather than attainable state counts. On-site local graph constraints, seam closures, marked states, and arithmetic precision still need explicit accounting. The range-two T32 ceiling should be read only for the indicated column-boundary/frontier representation, not as an established global peak over every intermediate update or a certified memory bound.

The 3 onsite/horizontal/vertical term types yield 9·32=288 ordered displacement insertions for full H′² after factoring out translation. Expanding 1+6+6 product terms yields the stated naive 32·13²=5408 insertions. Order matters on overlapping supports. Neither count measures runtime or includes a proved optimized contraction.

The second-order same-sublattice pair coefficient +g² n_uv/8 follows by solving 2a_uv+g z n_uv=0 at z=−g/4. Adding those pair amplitudes can cancel this leading residual only; finite-g complete cancellation or accuracy has not been demonstrated. A marked correction exp(zC†)(1+B†)|0> reproduces its specified q2 kernel but includes at most one B insertion in each layer, not exp(B†). The MPO upper dimension 2+3N=98, factor 9604 in the double layer, and (1+496)²=247009 independent bra/ket terms are formal upper constructions, not efficient certified algorithms. “Minimal” here means a targeted candidate correcting the identified channel, not an optimization theorem.

## Reproduction and resource scope

Run REPRODUCE.sh from this directory. The independent check imports no producer modules. Its original run used CPU6, 0.97 CPU seconds and approximately 48 MiB RSS, with hard limits 30 CPU seconds and 256 MiB. Only local 16×16 matrices and polynomial-size geometry enumeration are formed. A rerun's timing fields may differ. Producer artifacts remain frozen. All further physical fixtures, reachable-connectivity passes, and production contractions require the separately stated scope/approval gate.
