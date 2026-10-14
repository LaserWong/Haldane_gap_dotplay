Updated 2026-10-10 14:41 EDT (America/New_York) / 18:41 UTC.

# Independent audit. Spin-2 positive leading spatial atom

## Accepted result and scope

**PASS for the new analytic implication and four exact scalar exclusions, with
the original finite heat-trace and MPS certificates retained as inherited
inputs.** This review independently reconstructs the odd-length transfer
identity for the integer-spin model, so odd-length applicability is not merely
assumed on the basis of a finite table. The original many-body eigensystems,
exact MPS block construction, and Arb matrix powers were not recomputed here.
Their provenance, recorded certificate endpoints, dimensions, and all new
scalar comparisons were checked independently.

At beta = 8 and shift a = 4.76121, the same spatial transfer operator has a
positive maximal-modulus eigenvalue in its A4-trivial sector I, hence also in
its D2-trivial sector J. The four witness lengths give the following lower
bounds on that **same** eigenvalue.

| Physical witness length L | Positive atom is strictly above | U8 ell^(L-8) |
| --- | --- | --- |
| 128 | 0.971082 | 0.9998903610827924746489... |
| 256 | 0.985901 | 0.9997791028490990679963... |
| 512 | 0.993037 | 0.9995874464748997161941... |
| 1024 | 0.996540 | 0.9997585749306789008175... |

All inequalities are exact rational comparisons. The last column is a display.
The strongest combined conclusion is the last lower bound. A4-trivial does
not mean that the atom has been proved an SO(3) singlet. No simplicity,
spectral separation, spatial purity, thermal startup, or uniform physical gap
is established. The earlier I/P moment counterexample remains compatible.

The producer's general inequality needs one wording clarification.
**Both L and q must be even**. The actual application uses q = 8 and is valid.
No numerical producer file or frozen I/P witness was edited.

## 1. Model and all-integer transfer construction

The model is the unit-coupling periodic isotropic spin-2 chain,

    H_L = sum_j S_j dot S_(j+1),    S^2 = 6,
    Z_g(L; beta, a) = Tr exp[-beta (H_L(g) + a L)].

At L = 2, the two periodic bonds are counted separately. At L >= 3, only the
seam bond is rotated by g. The twists used here are identity, a pi rotation P,
and a 2pi/3 rotation C. All resulting physical Hamiltonians are finite-dimensional
and Hermitian, so every Z_g is strictly positive. This is positivity of a
physical partition function, not positivity of a unitary-weighted Gibbs trace.

The following gives the integer-spin extension of the archived spin-1 history
construction in [the earlier bridge](../../audit/APPENDIX_A_BRIDGE.md), without
assuming that a claim about spin 1 automatically applies to spin 2.

Spin 2 admits a real orthogonal rotation representation, equivalently a basis
where time reversal is complex conjugation. In that basis S_alpha = i A_alpha
with A_alpha real antisymmetric. Put B_alpha = A_alpha/2, so ||B_alpha|| <= 1.
The antiferromagnetic bond satisfies

    -S_j dot S_(j+1) = 4 sum_alpha B_alpha tensor B_alpha.

A bond history consists of p chronologically ordered times in (0,beta) and p
colors in {x,y,z}. Give it the positive measure 4^p dt_1 ... dt_p, including the
empty history. The total measure is exp(12 beta), hence finite. For two
neighboring histories x,y, merge their events in chronological order and set

    K_a(x,y) = exp(-beta a) Tr[chronological product of their B factors].

The product is real. Interchanging x,y leaves the merged sequence unchanged
outside equal-time coincidences, a null set. Thus K_a is real symmetric.
Its absolute value is at most 5 exp(-beta a). It therefore defines a real
self-adjoint Hilbert-Schmidt, and hence compact, operator X_(beta,a).

Absolute convergence of the Dyson expansion permits regrouping the events
bond by bond and site by site. Each bond contributes the stated measure and
each site contributes K_a. Consequently the cyclic kernel integral is exactly

    Z_identity(L; beta,a) = Tr X_(beta,a)^L,    every integer L >= 2.

There is no bipartite gauge or even-length restriction in this argument. In
particular, the same operator is used for odd and even lengths. The L=2 cycle
has two distinct bond histories and reproduces the parallel-bond convention.
Hilbert-Schmidt regularity ensures that X^L is trace class for all L >= 2.

The tetrahedral group A4 acts on the three colors by signed coordinate
permutations. On a history, multiply by the product of its color signs and
permute the colors. This is a real unitary group representation U_g on the
history space, since the measure is invariant. Rotation covariance of the
spin matrices gives U_g X = X U_g. Inserting U_g in the cyclic history
contraction applies that rotation on precisely one seam, so

    Z_g(L; beta,a) = Tr(U_g X^L),    every integer L >= 2,

up to an inverse convention that has no effect here. Pi representatives are
conjugate rotations. The two 2pi/3 inverse classes have identical physical
traces, also seen from the real structure of this representation.

A4 has irreducibles 1, 1', 1'', 3. Write I, O, O-bar, N for their self-adjoint
multiplicity-space spectra, each eigenvalue repeated according to its integer
multiplicity. Reality pairs O and O-bar with identical real eigenvalue lists.
The characters give, at every integer k >= 2,

    Z_identity(k) = I_k + 2 O_k + 3 N_k,
    Z_P(k)        = I_k + 2 O_k - N_k,
    Z_C(k)        = I_k - O_k.

Here S_k means the sum of kth powers in list S. Define J as the multiset union
I union O union O. Then J is the D2-trivial spectrum and

    Z_identity(k) = J_k + 3 N_k,
    Z_P(k)        = J_k - N_k.

All sector spectra have finite second, hence finite fourth, absolute moments.
These are actual compact-operator spectral lists. Arbitrary rationally
weighted moment measures must not be substituted in the attainment argument.

## 2. Positivity, compactness, and leading multiplicities

More generally, take real lists J,N with sum |lambda|^4 finite and the above
identities at all sufficiently large integer lengths. Let p_J be the supremum
of positive J atoms and r_J the supremum of their absolute values.

For all sufficiently large odd k,

    J_k = (Z_identity(k) + 3 Z_P(k))/4 > 0.

There must be a positive J atom. Fourth-moment summability bounds the list and
allows only finitely many occurrences above any positive modulus threshold.
Thus p_J > 0 is attained. If a negative atom -x had x > p_J, then, for odd k >= 5,

    J_k <= J_4 p_J^(k-4) - x^k,

which is negative for sufficiently large k. This contradiction proves
r_J = p_J. The proof permits infinitely many atoms accumulating at zero.

Similarly,

    I_k = (Z_identity(k) + 3 Z_P(k) + 8 Z_C(k))/12 > 0

on odd lengths, so r_I is attained by a positive I atom.

Even-length positivity of Z_P gives J_(2m) > N_(2m). If an N atom had modulus
x > r_J, then

    N_(2m) >= x^(2m),    J_(2m) <= J_4 r_J^(2m-4),

a contradiction for sufficiently large m. Hence r_N <= r_J. With C available,
the same argument applied to I_(2m) > O_(2m) gives r_O <= r_I. Then

    N_(2m) < I_(2m) + 2 O_(2m)
             <= (I_4 + 2 O_4) r_I^(2m-4)

gives r_N <= r_I. The maximal modulus of the entire spatial spectrum is
therefore attained by a positive I atom (or a positive J atom using I/P only).

No assertion about leading multiplicity follows. At nonzero leading radius r,
there are finitely many eigenvalues at +r and -r. Dominated convergence shows
that an odd-sector trace divided by r^k tends to m_+ - m_-. Positivity forces
m_+ >= m_-, but equality is possible. The leading odd terms may cancel while
smaller atoms keep the odd trace positive. For example J = {1,-1,1/2}, N empty
has strictly positive I/P traces at all lengths, but both signs attain the
norm. Nontrivial sectors may also tie. For example, I = {1,1}, O = {1}, N = {1} gives
Z_identity = 7, Z_P = 3, Z_C = 1 at every length. Thus neither strict dominance
over other sectors nor a unique leading atom may be inferred.

## 3. Atom exclusion and shift normalization

For **even q and L with L > q >= 4**, if every atom in the complete spectrum
has modulus at most ell >= 0, termwise comparison gives

    Z_identity(L; beta,a) <= ell^(L-q) Z_identity(q; beta,a).

All sector multiplicities are positive integers and both powers are even.
The formula is generally false for odd q because odd moments can cancel.

The dominance theorem makes an assumption of no positive trivial-sector atom
above ell imply that every atom is at most ell in modulus. Thus certified
Z_identity(q) <= U and Z_identity(L) > B exclude that assumption whenever
U ell^(L-q) < B. This does not need a separately small N-sector majorant.

Here q=8 and

    a0 = 5951/1250 = 4.7608,
    a1 = 476121/100000 = 4.76121,
    beta(a1-a0) = 41/12500,
    U8 = 3382547386422157/100000000000000.

The shift multiplies the spatial operator by the positive scalar
rho = exp(-41/12500), and multiplies its kth moment by rho^k. Therefore

    Z_8(beta,a1) = exp(-82/3125) Z_8(beta,a0) < Z_8(beta,a0) <= U8.

The old U8 is a conservative valid upper bound at the target normalization.
The verifier additionally encloses both exponential factors by exact rational
Taylor bounds. Those enclosures are not necessary for the conservative
inequality. Their purpose is to independently verify the normalization.

The producer used a floating exponential/logarithm only to propose a rational
millionth ell. This is harmless because acceptance is the exact Fraction
comparison U8 ell^(L-8) < 1. The independent verifier uses the four rational
ell values directly, never evaluates a logarithm, and also verifies
U8 (ell+10^-6)^(L-8) >= 1. Thus every quoted ell is the largest millionth that
passes with this conservative U8 and B=1. No floating logarithm is a premise.

## 4. Original finite-input provenance and Z_L > 1

### L8 heat trace

The original full trace-interval JSON has SHA-256
`ed30cdae706c3907c08f69fe6913e81ff22c3c69e7b53733a1ef8fe0e4967690`.
Its beta=8, L=8, identity-twist row has physical Hilbert dimension 5^8=390625,
shift 5951/1250, and exact upper endpoint U8 as above. The 14 beta=8 I/P rows
match the producer snapshot exactly. The row is an archived complete-spectrum
residual-validated enclosure, not an order-9/10 Ritz estimate.

The original finite-spectrum validation assumptions are preserved in
[ARCHIVE_VALIDATION.md](inputs/ARCHIVE_VALIDATION.md), including IEEE-754 and
interval-inclusion assumptions. They were not replaced by a claim of an
exact-integer heat-trace recomputation. This atom argument needs only L8 I. 
It does not use any unverified order-9/10 moments or a computed C trace.

### D124 variational certificate

The original D124 certificate and results summary agree exactly. Its integer
tensor and block text match both the certificate hashes and original archive
manifest, with the following identities.

- Tensor hash is `f82ed6c2160a25fae642b4dcde05ed3fa4e841acc92b4e5f66293159890b54dd`
- Exact block text hash is `cf79dc8f5723e180e49d506a2cfd00b8488be3f6f065e1f2e594b05391312c5d`
- Original Arb certificate hash is `2b7632e1f8040a5e48db77af5c0051a93636d83d48cd6d57a327b99d775c5b3e`

The witness is a single periodic MPS with virtual bond dimension D=124. Its
norm transfer acts on D^2=15376 dimensions, split into highest-weight blocks
of sizes 116,311,417,423,351,243,141,68,26,7,1. The maximum reduced block is 423.
These are not physical Hilbert dimensions or a 124-dimensional many-body
linear trial space. The physical length-L Hilbert space has dimension 5^L.

The source verifier computes

    v_L = sum_J (2J+1) Tr(T_J^L),
    u_L = sum_J (2J+1) Tr(T_J^(L-2) O_J),
    e_trial(L) = u_L/v_L.

This is energy per site. Its common power-of-two scaling of T and squared
scaling of O cancels from the ratio. The inherited certificate records
strictly positive norms. Its displayed Arb balls, parsed as exact rational
center plus radius, have upper endpoints strictly below -4.76121 at all four
lengths. The independent audit verifies those signs rather than trusting only
the stored `energy_less_than_minus_a` Booleans.

Let e_upper be such an endpoint and delta_L = -a1-e_upper > 0. The variational
principle gives E0(L) <= L e_trial(L) <= L e_upper. Hence

    Z_L(beta,a1) >= exp[-beta(E0(L)+a1 L)]
                   >= exp[beta L delta_L] > 1.

This conclusion needs only the exact positive exponent, not a rounded
exponential. As an additional check the verifier constructs rational lower
bounds on exp[beta L delta_L]. Their displays are approximately 1.0479057126,
1.0176351242, 1.0344928389, 1.0701753314 for L=128,256,512,1024. These stronger
numbers are not used in the four producer exclusions.

The archived norm positivity, exact tensor-to-block construction, and Arb
contractions remain inherited certificates. Rehashing their files is a
provenance check, not an independent derivation of those numerical inputs.

## 5. Portable exact replay and optional original contraction

The minimal review is entirely self-contained and requires only the Python 3.11+
standard library. Run the following commands.

    cd research_20261010/spin2_positivity_review
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python independent_audit.py

It runs with one CPU affinity, a 1 GiB address-space limit, and a 120-second
CPU limit. The observed runtime was about 1.2 seconds. It imports no producer
module, invokes no eigensolver, performs no new MPS matrix powers, and computes
no new heat trace. Results are in [audit_results.json](audit_results.json) and
[run.log](run.log). An optional `--archive /path/to/extracted/archive` rehashes
the original files as well. The original-source run is preserved separately.

The 54,961,019-byte block text is bundled as a deterministic gzip stream split
into 12 ordered parts, each at most 2 MiB, in
[blocks_gzip_parts](inputs/blocks_gzip_parts). The [part manifest](inputs/blocks_gzip_parts/manifest.json)
records the order, each part's SHA-256 and byte count, and both whole-stream
hashes. The compressed stream is 23,361,037 bytes, SHA-256
`736d7544363f65bd4c378973a727e5c417c9d0fcd04744ab15168b73b1b47423`.
The verifier checks every part and streams their concatenation through gzip,
checking the decompressed SHA-256, byte count, integer entries, and block
dimensions. It requires no external private path, reassembled gzip, or
uncompressed copy. No duplicate full gzip or block file is shipped.
To extract the block file explicitly, run the following commands.

    cat inputs/blocks_gzip_parts/part-*.gzpart | gzip -dc > improved124_exact_blocks.txt
    sha256sum improved124_exact_blocks.txt

The compressed stream itself can optionally be reassembled with the following commands.

    cat inputs/blocks_gzip_parts/part-*.gzpart > improved124_exact_blocks.txt.gz
    sha256sum improved124_exact_blocks.txt.gz

For a **fresh original Arb contraction**, which this review did not run, use a
separate directory and the preserved original verifier. Python-flint/Arb is
required. The archive used python-flint 0.9.0. This optional operation is larger
than the scalar replay and should retain one numerical thread, as in the following commands.

    mkdir -p /tmp/spin2_mps_replay
    cat inputs/blocks_gzip_parts/part-*.gzpart | gzip -dc > /tmp/spin2_mps_replay/improved124_exact_blocks.txt
    cp inputs/archive_mps124_integer_tensor.json /tmp/spin2_mps_replay/improved124_integer_tensor.json
    cp inputs/archive_mps_verify_arb_mps.py /tmp/spin2_mps_replay/verify_arb_mps.py
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python /tmp/spin2_mps_replay/verify_arb_mps.py --prefix improved124 --a 4.76121 --Ns 128 256 512 1024 --prec 256

The original exact builder, tensor, build log, Arb verifier, contraction log,
certificate, and README are included. The original full archive manifest is
also included, with SHA-256
`92c2cb80c718e5daf5c6e78a0dcddd220b643b5b974c9924b2699d2ab6953e1a`.
It authenticates the included original-file hashes relative to that recovered
archive. A self-contained manifest is not external proof of authenticity.

## 6. What remains open

This result repairs the leading-positive-atom localization step. It does not
repair the numerator-one thermal recipe defeated by the separate
[I/P moment witness review](../spin2_moment_review/README.md). That witness
already has a positive J-leading atom, so the two results are compatible.

Thermal startup and any uniform spin-2 gap remain unsolved. Additional thermal
or cross-temperature information, or a demonstrably stronger scalar method,
would be needed. This audit provides no reason to launch an expensive
higher-order heat-trace campaign.

The active tree is an exported workspace without `.git`. No branch or commit
was invented. The root README records the resumed source commit. All files
written by this audit are confined to this review directory, and no frozen
producer artifact was edited.
