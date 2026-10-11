# Physical-input reproduction: independent proof and acceptance conditions

Final verdict: ACCEPTED. All18 entries have independently validated physical matrices, orbit coverage, checkpoint identities, integer aggregates and exact error enclosures. The terminal producer export is verified against manifest17110955acc17821025bab5c1609706273510de6c8c2a31eb7184d693a9b9156. No unresolved physical thermal premise remains in the two scalar results identified below.

## Physical model and data provenance

The model is the periodic uniform spin-one Heisenberg chain with unit bilinear exchange. The two seams are identity I and a π rotation P on the closing bond, atβ49/4, shift a=700741/500000. Lengths4 through12 include odd sizes. Each physical Hilbert space has dimension3^n, and total magnetization is conserved. The runtime inputs are produced by the inspected real integer column kernel and strict runner. Their immutable source/binary/coefficient manifests are checked; no reference total participates in producing an individual column. The reviewer executes no heat kernel or imported scientific code.

The physical matrix in a weight block is D=32I−3nI−2H. Independently rebuilding its diagonal32−3n−2Σw_iw_(i+1) and hopping−2 (changed to+2 on the P seam) proves the stored matrix digests correspond to the intended Hamiltonian. The reviewer enumerates words in lexicographic/base-three order and constructs row neighbors directly from physical ladder rules, instead of executing the producer matrix-output command. Each entire sparse-matrix byte digest, dimension and stored-entry count is matched for both seams and all magnetizations0 throughn.

## Coverage and signed symmetries

A separate independent orbit enumeration uses cyclic shifts and reversal. Positive magnetization gets twice the dihedral orbit size to include its negative counterpart. At zero magnetization, global digit negation is included in the orbit itself and is not counted twice. Set cardinalities handle stabilizers. Independent lexicographic representatives, sorted codes and exact weights match every recorded sector, and their full weighted count is3^n. This check is made independently of the producer's case metadata.

Physical reversal and global spin negation preserve the relevant column norms. A signed cyclic shift restores the P seam by a π gauge on an arc. This works for odd lengths without a bipartite assumption. The accepted kernel review checks these symmetries explicitly on tiny odd/even matrices and analytically for every length here. Rounded integer columns need not be signed-shift equivariant: the error bound compares repeated selected exact columns with repeated computed representatives, so no such false assumption is used.

Every deterministic M/start/count batch must be present exactly once. Its payload digest, full case/source/kernel/coefficient/wrapper identity, matrix/orbit digest, exact ordered code/multiplicity slice, nonnegative integer norm and weighted aggregate are checked. No duplicate or omitted code is permitted across batches. The final case certificate must bind every batch payload digest and reproduce the full weighted aggregate W. A completed certificate file alone is insufficient.

## Exact approximation and errors

The inherited analytic energy bound0≤3n/2+H≤5n/2 makes R=D/32 a real self-adjoint contraction for4≤n≤12. The desired half-temperature heat operator is F=exp[98(R−I)]. The trace is Z_n(49/4,g)=exp[x_n]||F||_F² with x_n=(49/4)n(3/2−a).

The kernel uses conditioned rational Poisson weights p_j proportional98^j/j!, j0..280, coefficients c_j=floor(2^55p_j). The last nonzero integer coefficient is191; zero leading integer Horner steps may be omitted, while the error proof charges all281 rational steps. Truncation and renormalization operator error is<2^-84<2^-55. Mathematical floor of negative coordinates is essential and was independently tested.

With d_n=floor(sqrt(3^n))+1 and E_n=281(d_n+1)+1, every computed representative column X satisfies ||X−2^55F e_r||≤E_n. Repeating columns by physical multiplicities yields |sqrt(W)−2^55||F||_F|<d_nE_n. The real kernel's signed64 partial sums are protected by row bound76 and coordinate bound2·2^55; signed128 squares,64-term unsigned128 chunks and GMP aggregation are exact. These implementation bounds are independently accepted in the kernel review.

For r=floor(sqrt(W)), s=Σ_(j=0)^100 x_n^j/j!, t=x_n^100/100!, the inequalities0<x_n<15 and the geometric omitted-term bound give s≤exp(x_n)≤s+t. Therefore
L=s·max(0,r−d_nE_n)²/2^110,
U=(s+t)·(r+1+d_nE_n)²/2^110.
The reviewer computes these rational endpoints afresh and checks r²≤W<(r+1)². Each accepted physical interval lies strictly inside its published center±30·10^-6; the endpoint margins also exceed13·10^-6. Exact agreement of W with the published integer is an additional reproduction result, not a substitute for the physical matrix, coverage and error proof.

## Exact composition with the accepted scalar theorems

The physical intervals discharge both previously conditional results, without changing either frozen proof:

- uniform_second_initialization_review, manifest3e713b2de14407cca8c14e7236c23077998d29ea13268267626859fc5c23511b: gap23/5000=.0046 and a unique ground state for every integer L≥36.
- uniform_second_moment_review, manifestdbdea168300fa8a014c4a1fcbb72a6f64d1f8ddb3250949eeeed067d55c329de: gap107/5000=.0214 and a unique ground state for every integer L≥36.

These are spectral gaps of the untwisted periodic uniform spin-one Heisenberg Hamiltonian with bilinear coefficient1. A scalar energy shift does not change gaps. The stronger .0214 statement includes the weaker .0046 statement. No claim is made below36 or about minimum initialization size.

check_provenance.py verifies all five producer/reviewer seals used in this composition. For the first theorem, each new physical [L,U] lies in the exact published center±30·10^-6 interval appearing in its certificate. For the stronger theorem, matching the coarse intervals would be insufficient. Instead the script computes l=floor(10^18 L)/10^18 and u=ceil(10^18 U)/10^18 for all18 inputs. It then reconstructs every signed moment interval of J=(Z_I+3Z_P)/4 and N=(Z_I−Z_P)/4 for powers4..12. Subtraction reverses the P endpoint: N_lower=(I_lower−P_upper)/4 and N_upper=(I_upper−P_lower)/4. All18 signed moment endpoints match the frozen improved certificate exactly. Cross-sector independence is not assumed: interval arithmetic provides simultaneous valid enclosures of the actual sectors.

Both scalar proofs use the same72-site D26 periodic MPS input. Its physical contraction was previously rebuilt, as recorded in audit/APPENDIX_A_BRIDGE.md, and both accepted reviews pin the identical audit/mps/contraction.out SHA256. Here V72>0 and −700741V72−500000U72>0 are rechecked exactly. U72 is a SINGLE-BOND numerator; the total shifted Rayleigh quotient is72(U72/V72+700741/500000), not the unmultiplied per-bond value. That rational is identical in both accepted scalar proofs. No fresh contraction is claimed here. The negative variational value supplies an energy bound without assuming uniqueness; uniqueness is a conclusion of the thermal gap argument.

The all-integer scope inherits the source-verified physical transfer identity for every n≥4 and the accepted signed-transfer interpolation, finite windows and staggered S36/T72 recurrence in those reviews. Both scalar certificates cover every earlier window and an asymptotic tail from36864 atβ12544. This review replaces the thermal-input premises; it does not replace those analytic arguments by integer-total matching. Historical conditional records remain truthful descriptions of their original evidence state.

## Campaign accounting and reproducibility

The original21600CPU-second budget ended with16 full cases and two incomplete L12 attempts. The failed attempts retain7320 seconds each. The sealed partial review remains unchanged. Root explicitly authorized an append-only extension to43200 at00:16:28UTC, retaining the old16207 charged seconds and the original61-attempt prefix. The repaired bounded configuration was independently reviewed before resumption. The immutable final ledger has259 attempts,27543 charged seconds, no active attempts, no new failures after extension, and terminal ALL_CASES_COMPLETE_PRODUCER_REVIEW_REQUIRED. The final independent verdict in this document resolves that review-required status without modifying the production ledger. The two-worker256MiB and06:00UTC limits remained in force. Charged seconds include retained worst-case failed reservations and are not a measurement of successful kernel CPU alone.

campaign_snapshot.zip contains2979 immutable campaign files, including all2428 raw checkpoints,18 full certificates and the ledger/history/completion evidence. SNAPSHOT_SHA256.json records every original relative path and digest, identical to the producer export state map. The reader verifies the archive digest, unique exact membership, safe relative paths and every uncompressed file hash before materializing a disposable .replay_snapshot directory. All final completed-case and extension replays use this snapshot, not mutable production state. The scripts launch no heat columns. The source/binary/error proof dependencies remain separately pinned to their earlier accepted reviews.
