# Connected local-rule correctness prototype

Frozen 2026-10-11 02:00 UTC / 2026-10-10 22:00 EDT. Local compiler only; independent review pending. No full 8×4 support contraction, q6 cache, global q8/q10 enumeration, or 8×8 calculation was performed.

## Model and conventions

H′=Q+(g/2)(C+C†+D), K=[C,C†], E=[D,C†]. The compiler produces N=[C,[D,C†]], F=[[C,D],[D,C†]], L=[[C,[C,C†]],C†]. Each edge carries its actual integer weight. The 8×4 torus has 32 rungs and 64 unit edges. Small 4×2/5×2 comparisons retain doubled vertical edges.

The basis is orthonormal real spherical, rung states (s,t+,t0,t−), encoded (0,1,2,3). Pair creation is |t0,t0>−|t+,t−>−|t−,t+>; D swaps a singlet and triplet and acts as spin-one exchange on two triplets. These are exactly the already independently physically reviewed fixture conventions. This package does not convert its rules to Cartesian channels. Its two local matrix evaluators share the elementary action routine, so they are a cross-check of word cancellation/composition, not an independent derivation of the physical edge operator.

## Connected enumeration, signs and translations

Disjoint edge operators commute. N and L enumerate all connected-prefix ordered edge tuples, with repetitions allowed; F enumerates two internally touching pairs whose unions touch. F does not incorrectly require its third edge alone to meet the first pair. Commutators are expanded with their orientations and signs before collecting identical words. In each word, lexicographically minimal topological ordering of the noncommuting-letter dependency graph identifies only reorderings of disjoint edge letters. This is an exact trace-monoid equality, not graph-isomorphism identification.

For N/L the innermost C† edge is anchored; for F the C edge of E† is anchored. Each first-edge translation orbit on 8×4 has exactly 32 members because an undirected nearest-neighbor edge has no nonidentity translation stabilizer. There are exactly two representatives incident to 0 in the positive coordinate directions. Every full ordered tuple therefore has exactly one anchored representative and contributes with its actual weight. The compiler translates the support to the numerically smallest bitmask and carries the same permutation into every word. Ties are broken by translation index. Distinct point-group orientations are never identified.

Consequently the global operator is the sum of all 32 translates of every stored support operator. A support with nontrivial stabilizer causes no extra division: the original ordered tuple, not its unlabelled support, was quotiented. Local coefficients can encode several tuple representatives. In particular one must not apply a second /32 to embeddings after already storing these anchored templates.

A later invariant-support contraction may separately use sum_all_supports f=(32/q) sum_{0 in S} f, proved by counting (S,occupied rung) pairs. This is valid even for support stabilizers. When that reduction is used, every relevant translated operator embedding must still act on the target support. The two reductions are not interchangeable.

## Exhaustive local matrix checks

For every canonical support (at most five rungs, dimension at most 1024), the compiler constructs the complete sparse matrix by recursive action of trace-normalized words. It separately constructs the complete matrix of the untranslated-order signed words using iterative sparse column products. Exact integer map equality checks every nonzero entry and every omitted zero. The implicit full matrix comparison totals 121,251,328 entries; that count is not a count of dense allocated elements.

The compiler does not assert each individual canonical support matrix is Hermitian: a support with a translation stabilizer may require summing its translated embeddings before an adjoint identity is manifest. Global F and L orientation is verified by the physical comparisons. N is not assumed Hermitian.

Raw anchored ordered tuple counts N/F/L are 134/1242/1602, hence full counts 4288/39744/51264. Formal raw commutator word counts are 536/9936/12816. Identical-word cancellations within tuple expressions leave 536/9936/12520; subsequent disjoint-letter canonicalization and support collection leave 536/9798/6446 words. Canonical supports are 27/83/83, all survive. Matrix-unit transition counts are 6800/255819/34618. Maximum absolute combined coefficients are 6/48/36. There are 2/10/10 local vacuum-diagonal records.

## Serialization

Each rules_N/F/L.bin record is 12 bytes, little-endian on the recorded host: uint32 torus support bitmask, uint16 source local state, uint16 target local state, int32 signed coefficient. Local sites are increasing original rung index; rung digits use two bits. Records are ordered by support then source then target. A record represents the exact matrix unit on this support tensored with identity outside it. Files total 3,566,844 bytes, safely below the planned 16 MiB rule-payload ceiling. This is not a final occupancy/color pull index and is not a production matching-diagram implementation. Applying these files by scanning all records for every support is expressly forbidden.

## Independent previously accepted physical fixtures

validate.cpp re-enumerates full, unquotiented connected tuples on each small graph, combines by the exact support (translation canonicalization disabled), and compares pre-/post-cancellation local matrices. It then applies these matrices to the fixture's entire m=ψ6 vector. N/F/L output vectors agree exactly with direct sparse nested whole-operator compositions on both 4×2 and 5×2; this validates spectator identities and all signs/orientations for those nontrivial inputs.

Output-state counts N/F/L are 1931/3367/1281 on 4×2 and 3048/8484/3569 on 5×2. Expectations are N=6984/−684, F=−61656/−5688, L=41568/−33612. The accepted fixture is also replayed, and every one of its 15 signed terms plus m3/m4 and every sector norm agrees as exact JSON data. The nonzero 5×2 q10 term and the cancelling 4×2 q10 test are retained. Small reference fixtures do construct their own small q8/q10 comparison states; no such enumeration occurs on 8×4.

fixture_snapshot.cpp is the pinned accepted source with only an explicit return 0 appended to its former main, necessary because it is called as a renamed ordinary function. No frozen original was edited. The two physical outputs are not symmetrized fixtures and do not independently test translation reduction; that reduction is supported by the explicit orbit proof above and remains an independent-review target.

## Exact arithmetic and bounded resources

Local compiled coefficients are signed integers. On 8×4 at most 12816 formal word occurrences occur in a family, every word has length at most four, and every elementary absolute column sum is at most 3. A loose bound 12816·3^4=1,038,096 bounds each compiler matrix entry and partial absolute sum, well inside int64. Small-graph full tuple enumeration has at most 15·7·13·19 per nested family and the similar finite edge-pair bound is below 10^5, so 8·10^5·81<2^27 bounds raw local partial sums. Physical fixture amplitudes/dot products retain its accepted <2^40/<2^100 bounds, with checked int128-to-int64 amplitudes. No large optimized-witness amplitude is imported here; there is no asserted source int128 bound or GMP contraction implementation for production.

Every run is pinned to CPU6, single-threaded, RLIMIT_AS 256 MiB. Builds use a separate 512 MiB cap. Initial compiler, strengthened compiler, final checkpoint replay and small-fixture validation are all counted in resources_ledger.json. The attempt ledger conservatively charges exactly 30 CPU seconds (3+18+4+5); no budget remains. Recorded CPU checkpoints plus the small reference replay wall-time bound sum to approximately 28.19 seconds, excluding tiny finalization tails. No fresh runtime benchmark is authorized by this package. Compiler checks CPU between groups and every completed support; RLIMIT_CPU is a hard backstop. Allocation failure or assertion failure means incomplete, never accepted.

## Exact 15 Cartesian probe lemma

For q=6 let T=Σ_P a_P ∏_{(i,j)∈P}δ_{α_i,α_j}, where P ranges over the 15 perfect matchings and each Cartesian triplet label α_i is in {x,y,z}. For a chosen matching P assign x to its first pair, y to its second, z to its third. Each color appears exactly twice. A product belonging to another matching Q is nonzero only if Q pairs equal colors; this forces Q=P. Therefore the chosen evaluation is exactly a_P. The 15 evaluations form the identity matrix on the matching basis, proving linear independence and exact coefficient extraction without Gram inversion.

This lemma applies only after deriving rules directly in the independently reviewed Cartesian convention or proving an exact unitary basis conversion. The spherical 0,1,2,3 labels in this compiler are not Cartesian colors. No silent convention substitution is allowed. The lemma presumes an invariant tensor already represented by this delta-pairing span; for a proposed operator action, invariant preservation and the applicable even-rank invariant span must be established, not fitted from probes.

## Final checkpoint-hardening attempt

The complete strengthened run in run/ is the authoritative evidence, taking 3.46989 CPU seconds and 5120 KiB RSS. The optional compiler_checkpoint_candidate.cpp additionally preserves the latest checkpoint on abort and accumulates all final counters. Its replay reached the 4.5-second soft cap immediately after the last L support. It is preserved as incomplete in checkpoint_hardening_run/, with ABORT.json; no completion claim is made for that attempt. All three emitted rule files are byte-identical to the preceding complete run, but its counts.json is intentionally not treated as complete JSON evidence. The budget is exhausted, so this candidate was not rerun. The completed compiler source was restored verbatim from its pre-hardening version and is the source used by REPRODUCE.sh.

In run/checkpoint.json, aggregate expanded-word/vacuum/max-coefficient fields are zero because that version does not accumulate them across families; authoritative nonzero per-family values are in run/counts.json. This bookkeeping defect does not affect rule generation or exact comparisons and is an explicit independent-review item.
