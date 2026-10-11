# Complete residual-pencil planning and independent 4x4 fixture review

Scope: exact complete H'^2 assembly for the current16D4x4 ground basis; proof of the sector residual pencil and a resource-gate review of the shared-support implementation. No new gap or higher-coupling theorem is claimed. No8x4 support contraction is performed by this review. Producer4x2 fixtures and partial8x4 microbenchmark do not constitute a verified complete8x4 matrix.

## Why precisely one block is missing

Write H'=Q+tA, t=g/2. The pair basis B includes vacuum and q2 singlets; L=C†Bpair is q4, R=A44 L is q4, M=C†L is q6, and U=R+M. Every column is a global SU(2) singlet. Pair creation adds two triplets; preserving action preserves triplet parity. Therefore all columns belong to the FULL even-triplet, spin-singlet sector. The Hamiltonian preserves this sector, but not the finite16D/43D span.

With F=L*L, S=L*R, V=R*R, W=M*M, X=R*A44R, Y=R*CM, Z=M*A66M, put P=A44R+CM and T=C†R+A66M. The complete H'U image has mutually orthogonal sector components
 q2: t CR,
 q4: 4R+tP,
 q6: 6M+tT,
 q8: t C†M.

The q2 image lies in the complete invariant pair-orbit basis, whose Gram is Gpair. Since <Bpair,CR>=<L,R>=S, its complete norm matrix is D2=S*Gpair^(-1)S. There is no projection loss here: all spatially invariant q2 singlets are included. The remaining squared norm gives
 J_UU=16V+36W+t[8X+10(Y+Y*)+12Z]+t²[D2+P*P+T*T+(C†M)*(C†M)].

The coefficients10 arise from4 and6 triplet sectors and retain both orientations of Y. This exact expansion was derived before examining the producer output.

The signed hard-core identity
 (C†M)*(C†M)=(CM)*(CM)+M*[C,C†]M
is an identity of bilinear forms, obtained by polarization of the operator identity, not an upper bound. Its commutator includes negative same-edge and occupied-center terms. Individual commutator entries and eigenvalues may be negative; only the SUM is the positive q8 Gram. The review finds a negative diagonal in COMM, explicitly preventing silent removal of its negative part.

H'(B,L) lies exactly in span(B,L,U). Let W(g) be its exact column-coordinate image map and K(g) the first-moment matrix. Then GW=K[:,B,L], and every mixed second-moment row is W* K. The known principal block is W*GW. Only J_UU needs new support contractions. Solving for a projected image of U and using K G^(-1) K would omit positive residual norm. The audit verifies that J-KG^(-1)K is positive semidefinite and nonzero, including at g=0, because Q does not preserve the mixed U=R+M finite span.

## Independent complete physical matrix fixture

The immutable independently accepted complete residual engine is copied with source and binary hashes. It uses exhaustive q4/q6 supports and direct bilinear matching forms, independently implemented from the producer's shared matrix engine. The review evaluates five U basis directions and ten pair sums. Exact polarization recovers every entry of PP,TT,CMCM and signed COMM. All100 entries match the producer4x4 matrices. Each scalar run processes455 fixed-origin q4 and3003 q6 supports; complete norms use N/q translation scaling. The q6 enumeration includes supports with zero M family but nonzero T image.

All four new blocks and the q8 sum have their required symmetry checked; PP,TT,CMCM and q8 are tested by exact semidefinite elimination. Exact accepted geometry reconstructs the16x16 Gram and first moment, verifies positive rank16, and reconstructs all mixed second moments. Polynomial extraction at formal g=0,+1,-1 is algebraic and does not invoke a stability claim at those formal couplings.

The three complete H'^2 polynomial coefficients reproduce the previously independently verified optimized.105 vector's full second moment coefficient by coefficient. Every one of the15 polarization trial forms also matches direct q0/q2 assembly plus independently calculated q4,q6,q8 image norms at.105. Positivity checks at several rational couplings include negative and unstable formal g only as tests of the exact physical squared operator, not as spectral-comparison claims.

## Correct sector pencil implication

Let E0 be the physical ground energy in H' normalization. First establish global ground identification separately: an even-singlet physical Rayleigh value below the full-Hilbert r1 guarantees that the unique global level below r1 belongs to that sector. The full reference count permits at most1+3N levels below r2. Independently construct3N mutually orthogonal odd-mode/spin directions whose entire Rayleigh span lies below r2. Orthogonality and symmetry block structure make the individual mode bounds a subspace bound. Together with the identified ground this exhausts the allowed count. Consequently every other even-singlet eigenvalue is at least a=r2. Merely substituting r2 for a full-Hilbert second eigenvalue is invalid.

Under this established sector hypothesis and ell<a, define
 P(ell)=J-(a+ell)K+a ell G.
For a nonzero rational physical sector vector c, c*P(ell)c=<psi,(H'-a)(H'-ell)psi>. If E0<=ell and all other sector energies>=a, every spectral factor is nonnegative. A strictly negative value therefore proves E0>ell. Because J is COMPLETE, no residual component is omitted.

Writing rho=<H'> and v=<H'^2>-rho² gives the equivalent inequality
 c*P(ell)c/||psi||²=v-(rho-ell)(a-rho).
A negative value with v>=0 automatically forces ell<rho<a and is precisely a strict Temple improvement. The audit reproduces equality at the previously certified Temple endpoint and verifies opposite signs upon shifting ell down/up by10^-6. It also tests the counterexample spectrum(-2,0,3), a=2, ell=-1: the vector at energy0 has a negative pencil while the actual ground-2 lies below ell. This demonstrates the essential at-most-one-level-below-a sector requirement.

An exact PSD pencil at a chosen ell excludes a negative witness only in the current finite trial span and for that cutoff. It is not a physical no-go or a proof that all bootstrap paths fail. Floating eigensolvers may suggest vectors and endpoints but cannot replace exact sign certification or the global/sector spectral obligations.

## Shared-support safety and bounded timing interpretation

The producer accumulates each matrix bilinear on the same complete support stream, including all TT contributions when M vanishes. Skipping COMM on an identically zero left M amplitude is valid because that row contribution vanishes; it does not authorize skipping TT. Signed commutator symmetry must be checked before any symmetrization. q4/q6 origin scaling requires exact divisibility. Partial samples must remain marked partial and cannot be used as physical certificates.

The source's amplitude updates use checked32-bit bounds, with64-bit intermediate additions/products. Local graph weights are at most2, weighted degree4, and vacuum commutator weight at most3 sum w², so those update products fit64 bits. Each matrix contraction term is a product of two bounded32-bit amplitudes and a matching Gram entry at most27; after promotion its magnitude is below2^67. Even the deliberately excessive bound choose(63,5)*225<2^31 terms per entry stays below2^98; scaling by N<=64 stays below2^104, safely within signed128 bits. Accumulation additions are checked. The tiny direct L/M amplitude formulas involve at most three edge products and are independently bounded far below32 bits. Thus the new matrix accumulator is justified separately from any large-coefficient scalar residual bound.

The microbenchmark is a cost estimate, not a mathematical guarantee on full-run duration. A separately authorized hard CPU/memory cap remains mandatory. This review's15 independent4x4 support runs used3.24CPU seconds and9.5MiB peak RSS. Matrix assembly used below1CPU second and24MiB peak RSS; a250MiB address-space allowance accommodates NumPy mappings. No large physical contraction or8x8 residual is justified by this fixture.
