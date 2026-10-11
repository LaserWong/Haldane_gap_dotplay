# Correctness and sample scope

## Direct Cartesian convention

Each rung is (s,tx,ty,tz), labels 0/1/2/3. In two-spin bit coordinates, unnormalized norm-squared-two vectors are s={1:+1,2:−1}, tx={3:+1,0:−1}, ty={0:+i,3:+i}, tz={1:+1,2:+1}. Their tensor products have norm squared four.

The two-rung operator A=C+C†+D is checked against the physical four-spin operator P_(0,2)+P_(1,3)−I, which is twice the sum of the two intralayer spin-half exchanges. benchmark.cpp independently constructs all sixteen spin-basis columns using exact Gaussian integers and verifies every Cartesian matrix element after multiplication by the normalization factor four. This derives rather than simply imports the physical edge assertion.

C† creates sum_a |a,a> from |0,0>; C annihilates equal nonzero colors; D swaps one occupied rung and one vacancy, and on two triplets is the permutation minus the equal-color singlet contraction. Equivalently D|a,a>=−Σ_(b≠a)|b,b> and D|a,b>=|b,a> for a≠b. compiler.cpp implements these rules directly; there is no substitution of spherical indices for Cartesian colors.

The model and normal-ordering remain H′=Q+(g/2)(C+C†+D), K=[C,C†], E=[D,C†], N=[C,E], F=[E†,E], L=[[C,K],C†]. The signs/orientations of all commutators and the small graph's doubled width-two edges are retained.

## Connected compiler and translations

Geometry, connected ordered tuple enumeration and commuting-disjoint-letter canonicalization are copied from the independently accepted local compiler. Each full tuple is represented by its first designated edge anchored at one of the two positive origin directions. A first edge has a 32-member translation orbit on 8×4. Canonical support translation carries every local endpoint permutation explicitly; graph-isomorphic orientations are not identified.

Every local matrix is compared with the raw pre-trace-normalization polynomial through two exact integer composition paths. For N/F/L the complete local rule counts are 6824/263791/34618 on 27/83/83 support blocks. Records retain the predecessor's 12-byte little-endian format: uint32 support, uint16 source, uint16 target, int32 coefficient, with sites in increasing order. Each is tensored with identity on external spectator rungs.

The rule actions use all 32 translated embeddings per block: 864/2656/2656 embeddings. For each family exactly one block has a fourfold support stabilizer; the code explicitly finds all translations preserving every support and asserts that any nontrivial stabilizer has order four. It does not divide these duplicate support masks away: their site-label permutations may differ and belong to different tuple contributions. For F/L, summing the local matrices over the support stabilizer gives an exactly Hermitian matrix. This verifies the relevant orientation at the stabilized blocks. N is not presumed Hermitian. No additional factor 1/32 is used in applying embeddings.

Origin-containing target supports are a sampling convention only. No sampled checksum is multiplied by 32/6 or promoted to a complete contraction. A later invariant density sum would use the separately proved occupied-site double-counting factor while retaining all relevant operator embeddings.

## Fifteen exact probes, including physical-vector tests

For six occupied rungs the invariant matching tensor is Σ_P a_P Π_(i,j in P) δ_(alpha_i,alpha_j), with 15 perfect matchings. Assign distinct x,y,z colors to the three pairs of a chosen P. Since each color occurs exactly twice, every other matching Q has a zero delta product; the P product is one. That probe is exactly a_P. The 15×15 probe evaluation matrix is explicitly asserted to be the identity.

On each small fixture, the entire m vector and the entire compiled N m, F m and L m outputs are reconstructed by extracting these probes separately on every occupied support, expanding the resulting 15 delta-pairing channels into all 27 pair-color assignments, and comparing the resulting full sparse vector exactly. This is a test of the invariant-span premise and coefficient extraction, not merely a fit on the 15 probes. The compiled vectors also equal direct nested whole-operator compositions.

Both accepted physical 4×2/5×2 fixtures are reproduced. Every one of their 15 separate signed terms, m3/m4, and sector norms equals the previously accepted answer. The maximum number of nonzero Cartesian sparse states differs from the spherical implementation, as expected for a change of basis; analyze.py excludes only this diagnostic when comparing otherwise identical fixture JSON. The 5×2 q10 test is nonzero, and the 4×2 q10 cancellation is preserved.

Small physical comparison states may occupy q8/q10 on eight/ten rungs. No such global states are constructed on 8×4.

## Pull index and vacuum treatment

The in-memory index groups each local matrix by target color state, yielding short lists of source local states and signed coefficients. Every translated embedding is listed in the incidence indexes of its occupied geometric sites. For a six-site target S, scan those six incidence lists and accept an embedding only at min(B intersect S). Thus every embedding touching the target is visited exactly once, without scanning the full rule table. Its target occupancy and color digits select the row before any source lookup.

For a selected source local state, the source global state copies target spectators unchanged, removes the target's local digits, and inserts the source digits on the embedding's ordered sites. Since N/F/L preserve occupation, the source support has exactly six sites. An analytic source evaluation supplies its scalar Cartesian amplitude, which is multiplied by the signed rule coefficient. Repeating this for the 15 probes yields the output matching coefficients.

Vacuum-diagonal rows are removed from the ordinary transition lists. For coefficient c on B, c Π_(i in B)(1−n_i) is expanded into occupation-subset monomials with alternating signs. All translated identical subsets are combined exactly. The constant is evaluated directly; nonempty subsets are indexed by their minimum site and accepted only if contained in the target S. Every sample checks this result against a direct scan of the small embedding geometry testing B intersect S empty. This diagnostic scan does not inspect transition tables or source states. Reported vacuum_polynomial_terms are map-key counts before removing zero coefficients; the actual pull index skips zero coefficients.

The index is logically derived from the fully checked local matrices. The whole translated 8×4 sampled action is not independently recomputed by a second implementation in this producer package; that is an independent-review target. Small fixture column application and full-vector checks are a separate action implementation, but use their own small graph without translation quotienting.

## Analytic source and cache

The 14 cM coefficients are copied from the previously reviewed reference file and checked equal to the final 14 coefficients of the accepted 57D g=11/100 witness in bilayer_split_pencil_optimization/result.json. Coefficient order is B15,L14,R14,M14; cR is not substituted for cM.

For matching P with three pairs e_k, the M coefficient is Σ_k 2 w_(k+1) w_(k+2) cM_(orbit(e_k)). Geometry and pair-orbit labels come from the pinned 8×4 geometry. A scalar Cartesian amplitude sums only channels whose paired source colors agree.

The lazy unordered cache is keyed by the full 32-bit source support, stores all fifteen int64 channels, and is cleared at 16384 entries. It is not an origin-normalized full q6 cache. A target sample may require many neighboring source lookups; 512 limits target supports, not the number of source requests. Maximum storage is bounded by 16384 entries and observed runtime RSS. Across the three families there are 29650977 source requests and 265383 cache misses, a 99.10498% hit rate. The cache is reset between families. No full support sweep occurs.

## Sampling, arithmetic, and measurements

Targets have origin occupied and colex ranks floor(j·169910/511), j=0,...,511, among the C(31,5)=169911 possibilities. These are 512 distinct dispersed supports, including both extremes, not a random representative sample or a worst-case certificate. Their occupied-edge counts 0/1/2/3/4/5/6/7 occur 55/131/176/111/28/9/1/1 times. Of these, 285 have m identically zero and 227 nonzero. All 512 are processed in every family; no M-active filter is used to omit targets. Full geometric class multiplicities were not enumerated because a full support pass is outside scope.

Source channels obey |a_P|≤6 max|cM|<2^33, and source amplitudes obey |a|≤15·6 max|cM|<2^37. At most 100000 full connected tuples, eight signed words each, and 3^4 elementary color branches give a loose per-probe action bound below 100000·8·81·2^37<2^64. Thus signed int128 action accumulation is safe, while the source channels safely fit int64. Local rule coefficients are explicitly checked before serializing int32. The small physical fixture's checked int64 amplitudes/int128 dot products retain its previous conservative bounds.

The final sample checksum uses the exact matching Gram matrix 3^(number of union loops), not an unweighted coefficient dot product. Signed int128 amplitudes are imported into GMP by two uint64 words with explicit sign; no narrowing through signed long occurs. These checksums sum only the selected support bilinears and are not physical full moments. Source and action integers used one GMP limb in the observed import; products and accumulated checksums may use more limbs. gmp_max_limbs reports only imported action integers, not a bound on the final checksum.

Sample timing includes incidence/vacuum checks, row application, lazy analytic source lookup, exact Gram/GMP checksums and JSONL checkpoints. Per-support cpu_seconds excludes its subsequent GMP checksum and output. Setup timing includes motif generation, two local-matrix checks, indexing, stabilizer checks and rule serialization. Cold/warm lookup timings include target unranking and loop overhead; they are diagnostic batch timings, not isolated machine-instruction costs. Whole-run RSS is measured, not estimated from payload alone.

## Conclusion and limitations

run/analysis.json gives an empirical 2716.66-second sum for these three actions across all origin targets, or 27166.62 seconds with a tenfold margin. Setup adds 3.751678 seconds. This already fails the proposed 180-second gate and omits generic chi/v work, other moment terms, full-cache construction and independent production review. It does not show that exact moments are intrinsically infeasible or prohibit a future larger budget with a credible complete cost model.

No new .11 energy endpoint or all-size gap statement follows. The next proposal is a compact invariant-diagram compiler, not immediate production.
