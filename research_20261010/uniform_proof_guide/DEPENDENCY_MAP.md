# Proof dependencies and exact evidence identities

All paths below are relative to `research_20261010/`, except where explicitly marked repository-relative. The hexadecimal identity is the SHA-256 of that package's `MANIFEST_SHA256.json`. Individual consumed files and original Git blobs are pinned in `SOURCE_PINS.json`.

## A. Accepted theorem and the finite-size union

| Ingredient | Exact scope used | Evidence | Manifest SHA-256 |
|---|---|---|---|
| Final composition | Gap 31/1250, unique ground state, every integer L >= 2 | `uniform_gap_0248_all_sizes_review/PROOF.md`, `results.json` | `5407745b521a61a310d89857da94c14a73fcc2093a80d467dc8f72e9fd31deaf` |
| Strong producer | Own-length 26–33 trials, cached 4–25 stronger-gap recheck, n34 tail | `uniform_gap_0248_all_sizes/certificate.json`, `cached_prefix.json` | `659d03dd58275338f0a13af5fde6f6e503bca8eb7c3ac5d044a0e98e788e8ab1` |
| Analytic 2/3 and direct 4–23 | Unique ground state at each stated length, exact lower purities retained for stronger recheck | `uniform_small_lengths_completion_review/PROOF.md`, `results.json`, `anchors.out` | `b5225681662482e5ed219fe85d0cc9247703b21b183f6e6441dd081b7bc9d984` |
| Isolated 24 | Exact 24-site lower purity from the n24/48 pair, not a successful n24 infinite bootstrap | `uniform_n24_second_coverage_review/PROOF.md`, `results.json` | `9d31eeb0dc44f24047943a4ad4dd06e4f8f82aced5ca321857a1aaedf82b8282` |
| Direct 25 | Exact own-length trial with positive shifted energy and neighboring even-trace denominator | `uniform_direct25_coverage_review/PROOF.md`, `results.json`, `anchor25.out` | `a70156f108be662bbb9873ce12f9701701efd0b6680d2d187e677fa1e37b3cc9` |
| Infinite n34 tail | Every integer L >= 34 at 31/1250, canonical S34/T68, closure from 17408 at beta 6272 | `uniform_smaller_second_initialization_review/PROOF.md`, `scalar_results.json`, `anchors.out` | `54401c08804d8cade3cd91f652c2ae4d9182ceb25599e153802cc1a1770ffa2f` |

The final union is exactly `{2,3} union {4,...,25} union {26,...,33} union {L >= 34}`. The prior weaker gap labels at finite lengths are not the stronger proof. The final reviewer explicitly rechecks their accepted exact purities at beta times gap = 1519/5000.

The n24 package pins its fresh independent 48-site contraction through `uniform_n28_second_initialization_review`, manifest `e22c642a814744fed23e45e799b58be4d31da7c4e1b341e2d4c39b95bb474ead`. Its parity-specific window argument is inherited from `uniform_n26_second_coverage_review`, manifest `b4e4bc246acb27b63bb51745c23cbd28b7b0928d5d45ad19ddfb3ffe5d6d077d`. The guide explicitly derives the even-L24 bound, so no unproved physical purity monotonicity is hidden in this dependency.

Length 25 has mathematical acceptance and a separate unresolved resource-limit anomaly. Its reported 25.9614 process CPU seconds is not accepted as compliance with the asserted 15-second cap. The later guarded 26–33 result is separately accepted and does not erase that record.

## B. Shared physical and analytic foundation

| Ingredient | What it establishes | Evidence | Manifest SHA-256 |
|---|---|---|---|
| Original source scope | Untwisted physical transfer identity for every integer L >= 4. Original gap theorem itself has even-length scope | `uniform_source_scope_review/SOURCE_SCOPE.md`, `sources/model.tex`, `sources/transfer.tex`, `sources/introduction.tex` | `7c3ca3698dc82ace47e5c76482910404df1e1655e40ef6bc89f5775b2a5358c9` |
| Full second-input thermal reproduction | All 18 beta 49/4 identity/pi-seam inputs at 4–12, physical matrices, orbit coverage, 2,428 checkpoints, error intervals and refined signed-moment mapping | `uniform_second_thermal_full_review/PROOF.md`, `provenance_results.json`, other sealed review outputs and `campaign_snapshot.zip` | `792127565ad16526eeaa61add62bcc15db499578fc9d2157f11df27848867b94` |
| Signed moment analysis | Unit-occurrence support filters, signed interval directions, whole-domain long majorants and n36 continuation | `uniform_second_moment_review/REVIEW.md`, `results.json`, original source snapshots | `dbdea168300fa8a014c4a1fcbb72a6f64d1f8ddb3250949eeeed067d55c329de` |
| Signed moment producer | Exact rational filters, refined moments and polynomial coefficients | `uniform_second_moment_optimization/certificate.json` | `dc81945f85281a33df1b272a7a054b6f5d9b5fa32e8c7a1868c26e07bc97ec85` |
| Smaller-start producer | Exact n30, n32 and n34 states, windows, terminal conditions and 26 even majorants | `uniform_smaller_second_initialization/certificate.json`, `long_certificate.json` | `fcf4d2c7f838a8ee154f297549f3049a93b49cae30e758534edc9c3dc2d74a84` |
| Small-length producer | Direct 4–23 trial/trace certificates and 14 additional majorants | `uniform_small_lengths_completion/certificate.json`, `long_certificate.json` | `71606fa80898fb73b6f0fffb359480a1d3e716d98c47791d16d3470618c4af08` |
| Original second-route scalar replay | Credits the pre-existing n36/72 initialization and records the original log(20)/784 theorem | `uniform_second_initialization_review/REVIEW.md` | `3e713b2de14407cca8c14e7236c23077998d29ea13268267626859fc5c23511b` |

The older scalar reviews preserve their original conditional wording. The full physical review explicitly discharges their thermal premises rather than editing those historical records. The thermal review's further physical kernel and campaign provenance dependencies are pinned in its own `DEPENDENCY_SEALS.json`, `INPUT_SHA256.json` and `PROVENANCE_INPUT_SHA256.json`. The guide does not flatten those physical checks into a claim that agreement of integer totals alone suffices.

## C. Original-source pins and attribution

The source is the public `openai/math` September 24, 2026 Haldane-gap directory. Exact unchanged local bytes, SHA-256 hashes and links appear in `SOURCE_PINS.json`.

| Original file | Git blob SHA-1 | Principal use |
|---|---|---|
| `build/model.tex` | `f11cff765b71f52b913e389d4471655679c95274` | Hamiltonian, seam, shift, energy bound |
| `build/transfer.tex` | `41e01eee2b9103fd61201931005bd1b079b51cf1` | Real self-adjoint history transfer, all-integer identity from 4, sectors |
| `build/introduction.tex` | `1f1fcfc19bf92edcdcbe16c39928bc8da33678df` | Original theorem and exact comparison constants |
| `build/initialization.tex` | `a9a4604db87448b4e7d211ef483518b57862f097` | Original n60 and n36 second initialization, filter and packing framework |
| `build/thermal72.tex` | `b9f3c87a4fcfa96a82cdb5d4daf30b6088428037` | Original matrix-polynomial thermal certification without full ED |
| `build/trials.tex` | `14be92f2308bc6758f3aac628e337a363caead77` | Fixed D26 tensor and exact norm/single-bond/total-energy conventions |

The original TeX snapshots remain in their existing source directories with unchanged Apache-2.0 licensing and attribution. This package does not copy or modify those source files. The original n36 second initialization is not attributed to the new work.

## D. What this guide's self-check establishes

The self-check verifies pinned file identities, exact extraction and elementary scalar consequences with standard-library rational arithmetic. It includes the 40 rational Bernstein majorants, the n34 recurrence/window/closure conditions, all 30 finite purity bounds at the stronger gap, the exact small-volume angular-momentum calculation and rational logarithm-ratio enclosures.

It reads the accepted physical integer outputs as data. It does not regenerate physical matrices or heat columns, perform MPS contractions, validate every low-level compiled operation, or claim a second independent physical audit. Its new mathematical exposition still requires the separately planned independent review. Resource limits for the self-check are 60 CPU seconds and 256 MiB address space, with observed use reported in `SELF_CHECK.json`.

The first guide-specific self-check and its exact script are preserved in `history/`. Its observed process CPU was 30.21035921 seconds against a declared 30-second limit, so strict measured 30-second compliance is not accepted. It has no external wait4 or retained post-exec limit record, and no cause is inferred. The subsequently revised 60-second replay is a distinct run. Neither record changes the previously accepted theorem or resolves the older length-25 exception.
