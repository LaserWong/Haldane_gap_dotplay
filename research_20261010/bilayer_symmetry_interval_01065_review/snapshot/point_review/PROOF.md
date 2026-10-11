# Independent rational-vector point audit atg=.1065

## Accepted result

For the ordinary isotropic periodic bilayer, unit rung exchange and g=213/2000=.1065, every integer square sideL≥2 has a unique full-Hilbert ground and gap at least5362952719/250000000000=.021451810876.

This is a coupling-point theorem. It does not by itself extend any continuous coupling interval. No physical support contraction, eigensolver or vector optimization is performed by this reviewer.

## Exact new vectors, independent of the optimizer

The producer package c88289ad94b4d1370f1e6797488f794f9c0dc6e6a41c0bad3fefb68f007ee387 is pinned. The accepted previous point review and all its complete matrix/geometry/odd-polynomial dependencies are copied and verified. The new producer floating eigenvectors and scalar search are treated only as proposals. The reviewer never executes them or uses a floating residual or eigenvalue as a certificate.

For each N=16 and32, both saved energy and pencil candidate integer coefficient vectors are contracted exactly against the independently accepted Gram, affine H′ and complete quadratic H′² matrices, of dimensions21 and57. Norms are strictly positive. Every saved normalized mean, complete second moment, full variance, reference cutoff and affine/quadratic coupling coefficient agrees with a fresh rational contraction. All complete variance coefficient forms are positive semidefinite and all point variances nonnegative. The complete H′² matrices include all physical q8 and cross terms; projected H′ squared is not substituted.

For each of the four candidates, let a=r2, rho=<H′>, v=<(H′−rho)²> and ell be its saved strict endpoint. The checker verifies rho<r1<a, ell<rho−v/(a−rho)<a, and

<H′²>−(a+ell)rho+a ell<0.

The two selected candidates are precisely those with the larger exact lower rho−v/(a−rho); both are pencil candidates. Their lower-energy improvements are compared exactly with the energy candidates. The labels “optimized” carry no assertion of global optimization.

Every basis vector is an even singlet in the accepted full physical model, so any exact linear combination preserves that sector. The cutoff a applies to the full untruncated even-singlet sector, not to a projected matrix spectrum. Its validity and global-ground identification are checked as below.

## Numerator and spectral completeness

The new numerator is a43D integer vector. The reviewer independently rebuilds the8×8 weighted physical pair graph and pair-orbit first-H action from accepted geometry, embeds U=R+M into the57D split basis, and contracts the numerator's exact norm and affine energy coefficients. They agree with the saved43D Rayleigh data at the new coupling. This is a valid physical energy upper without a residual requirement. One numerator state is retained; the largest full physical Hilbert dimension is2^128.

All odd-mode Grams, means and full residual polynomials are reconstructed from the fixedz=.1 accepted structural identities, in exact Q(sqrt2). Positive Grams and complete variances are checked, and all16/32 momentum modes lie strictly below the newly evaluated global r2 cutoff. With spin multiplicity3 there are48/96 such odd states. Combined with rho<r1 and full-Hilbert comparison counts, this identifies a unique global ground and bounds the next even-singlet energy byr2. It does not assert full-Hilbert λ2≥r2.

The odd energy lower is max(r1,theta_lower−variance_upper/(r2−theta_upper)). The trace retains49/97 states including the ground and retains every omitted q=2,…,N tail term with multiplicity binomial(3N+q−1,q). The total reference count is at least4^N. Every new-coupling cutoff, count, odd lower and tail value is freshly checked.

## Trace normalization and exact size coverage

Each denominator trace pivot is the verified Rayleigh energy of its energy candidate. Its ground exponential width is pivot minus the selected pencil candidate's proved lower. All odd and omitted energies are normalized by the same pivot. The correlated exponent combinations are reconstructed as8e16−2u64,16e16−4u64,4e32−2u64. Ground, odd and full-tail exponentials atβ0,2β0,2β0 give fresh directed J1,J2,C0 lower bounds.

The selectedβ0=189/20 gives the first square base(8,8,189/10). The independently accepted square-symmetric recurrence and finite-window formula are used with exact raw txy/canonical labels; no rectangular axis is mislabeled. All initial ratios, raw/canonical states, defects and window purities match the independently rebuilt60-decimal values.

The four windows[8,16],[16,32],[32,64],[64,128] have exact gaps .093380470373, .060359036214, .043391979956 and .035821459633. Every window is accepted by exp(βγ)(1−p)<p withp>1/2, using the independent544-bit exponential implementation. The signed-transfer theorem covers odd integer sides as well as even ones.

At side128, β=1512/5, the canonical defect satisfies0<u≤1/500 and exp(βγ)*32u<1 forγ=.021451810876. The accepted asymptotic theorem covers all larger sides. The already proved short theorem on[0,.15] gives .050426624396 forL=2,…,7, larger thanγ. Hence no integer size is omitted.

## Resource and scope

The clean exact audit uses under3CPU seconds and21MiB RSS onCPU4, below the assigned120CPU-second/256MiB bound. REPRODUCE.sh verifies all seals and repeats the contractions and full physical/scalar checks in a fresh directory. Other floating proposals or possible higher couplings are outside this acceptance. A continuous [.106,.1065] result requires its separate endpoint/interior-control audit.
