# Original-source scope reconciliation and numerical comparison

2026-10-10 18:39 EDT / 22:39 UTC. Immutable supplement to the sealed uniform-chain reviews.

## Resolution

The original paper's final gap theorem is stated for even periodic lengths. Its spatial-transfer proposition, however, explicitly proves the untwisted physical trace identity for every integer n>=4, without an evenness restriction. The original source therefore supplies the odd-length identity required by our separately proved signed-spectrum interpolation. The accepted new all-integer scopes beginning at52,54,56,60 remain valid.

This conclusion follows from independently fetching and reading the actual model and transfer sections, not from assuming that a positive physical odd partition function equals an auxiliary odd transfer trace. No restriction to even lengths is required after this source check. Conversely, no odd-length gap theorem is attributed to the original paper: the odd extension belongs to the later interpolation argument in the sealed reviews.

For this supplement the inherited physical trace identity is expressly restricted to the original proposition's n>=4. Earlier local reports used the broader n>=2 convention. That broader endpoint is unnecessary here and is not justified by merely citing this source. All new gap ranges start at52 or larger, so this narrower source floor changes no accepted conclusion.

## Immutable source identities

Fetched through the GitHub connector from openai/math, under preprints/The-periodic-spin-one-Haldane-gap-September-24-2026:

- build/transfer.tex: Git blob `41e01eee2b9103fd61201931005bd1b079b51cf1`
- build/model.tex: Git blob `f11cff765b71f52b913e389d4471655679c95274`
- build/introduction.tex: Git blob `1f1fcfc19bf92edcdcbe16c39928bc8da33678df`

Verbatim source snapshots are included under sources/. The checker recomputes each Git blob SHA-1 using the exact byte length and Git blob header, in addition to recording SHA-256. SOURCES.json gives the verified official URLs. These hashes pin content independently of later branch movement.

## Why odd traces are the untwisted periodic physical trace

The model section defines H_n(g) for n>=4 as the ordinary periodic Heisenberg Hamiltonian with only its last bond conjugated on site0. It explicitly identifies H_n(I)=H_n. Its shifted Z_n(b,g) is a physical Gibbs trace and is strictly positive.

In Cartesian coordinates, G_alpha=i S_alpha is real, and

    -h = sum_alpha G_alpha tensor G_alpha.

The same factor occurs on both endpoints of each bond. This is an onsite basis choice, not a staggered rotation, bipartite sign transform, or alternating change of variables. There is no leftover twist when the ring length is odd.

The transfer section defines a bond history as an ordered list of times and labels. Its positive history measure has finite mass exp(3b). The kernel k_b(x,y) is the trace of the chronological product obtained by merging the two histories. Exchanging x,y leaves that merged chronological list unchanged. Therefore the kernel is real symmetric. No transpose or reversal of the local chronological matrix product is used to obtain symmetry.

The kernel is bounded in absolute value by3, so its integral operator is Hilbert-Schmidt on the finite history measure. Its cycle trace is the integral of the cyclic product of site kernels. The proof uses a product of Hilbert-Schmidt operators, so it does not assume an unjustified diagonal trace formula for the original kernel.

Expanding the physical Gibbs exponential into ordered bond events and regrouping by bond reproduces exactly that cycle integral. Absolute traced contributions at total degree k sum to at most3^n(3nb)^k/k!, so regrouping and integration are justified. At a site the chronological factors are precisely those from its two adjacent bond histories. This reasoning is independent of parity.

The seam identification is also explicit: the source rotates only the seam history's factor on site0 and matches it to the unitary U_g in the cycle trace. Reversing the spatial enumeration matches the factors using kernel symmetry; chronological products are not reversed. With g=I, the seam is untwisted. Multiplying by exp(-abn) then gives

    Z_n(b,g)=Tr(X_b^n U_g) for every integer n>=4,
    Z_n(b)=sum_i lambda_i(b)^n for every integer n>=4.

The proposition states both equations without parity restriction. Evenness is introduced only later when nth transfer powers are normalized as a probability distribution. It is essential for those probabilities, not for the physical trace identity itself.

## Why the signed interpolation is now licensed

At an even seed n, sufficient purity of the normalized nth powers of X_(2beta) identifies a unique largest-modulus eigenvalue. If that eigenvalue were negative, the signed leading term would make all sufficiently large odd traces negative. The absolute relative tail tends to zero: compactness supplies strict subleading modulus, and an even trace-class moment supplies a summable dominating sequence.

The source identity above applies to those odd lengths, and their physical Gibbs traces are positive. Hence the dominant eigenvalue must be positive. This is precisely the additional sign inference used in uniform_cooled_seed_review/REVIEW.md and uniform_seed_frontier_review/REVIEW.md. Their signed-tail bounds and absolute-spectrum Hölder interpolation then cover every integer in each advertised window. The seed recurrence still uses only even bases and correct staggered coordinates S(n,beta), T(2n,beta).

No new source hypothesis or numerical certificate is required. All prior accepted review manifests are rechecked unchanged by verify.py.

## Even-length fallback does not depend on the odd identity

The numerical bounds also survive if one deliberately restricts the conclusions to even L and refuses any odd-length premise. At even L, the leading contribution is |mu0|^L and every residual eigenvalue contribution is nonnegative. The even numerator bound is therefore at least |mu0|^L without the signed-tail subtraction. The same even endpoint moments and Hölder denominator estimate remain valid.

In the earlier notation this gives an even-window purity lower bound at least min(S sqrt(d),d), stronger than the used (1-rho) min(S sqrt(d),d). Thus every stored finite-window constant remains conservative on the even subset without knowing the leading eigenvalue's sign. The same argument supplies the even small-defect continuation. No numerical gap constant relies essentially on odd positivity; only extending its scope to odd lengths does. That extension is now supported by the directly checked all-integer source identity.

## Precise comparison with the original stated theorem

The original introduction's theorem gives unique ground states and two numerical bounds:

| Original scope | Original gap lower bound | Decimal display |
|---|---|---:|
| Every even L>=60 | (4/105) log(80/79) | 0.0004791917031184807 |
| Every even L>=2304 | log(20)/784 | 0.0038210870836147843 |

Our reviewed n60 result gives gap>=51/5000=0.0102 for every integer L>=60. On the directly shared even-length scopes, its certified numerical constant is approximately21.2858443366621 times the original L>=60 constant, and2.66939741932045 times the original eventual L>=2304 constant. These are ratios of proven lower bounds, not estimates of the true physical gap. The source's first and second inequalities are strict; the displayed new bound is a conservative non-strict rational endpoint.

The separate reviewed bounds gap>=0.0068 for L>=56, gap>=0.0025 for L>=54, and gap>=0.0038 for L>=52 extend the starting-size coverage, with their own stated numerical constants. They must not be substituted as a single constant on all smaller sizes. None certifies lengths below52 or proves that52 is the minimal possible seed.

The archived0.005908566393 bound beginning atL1920 is a later independently strengthened reproduction. It is not the original paper's theorem and must not be used as the original-theorem comparator. The original paper also observes a positive infimum over the finitely many remaining even sizes below60, but does not provide a common numerical value or uniqueness claim there. Our new explicit bounds do not replace that observation with a below52 certificate.

`verify.py` encloses the logarithms using a100-term rational atanh series and an explicit remainder. It verifies source byte identities and prior review seals. results.json records exact comparison intervals. This supplement makes no new physical computation and changes no previous sealed file.
