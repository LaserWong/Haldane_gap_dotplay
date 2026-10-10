# Complete second moment before further energy-only growth

Planning only. No new physical contractions or full second-moment matrices are claimed.

## Recommendation

Compute the missing complete H'^2 geometry for the CURRENT B,L,U=R+M basis on 4x4 and 8x4 before increasing the search dimension. This enables direct optimization of a certified ground lower endpoint. The cached split-basis Rayleigh tests improve energy by only 10^-6 at g=.11/.12. These energy gains do not measure possible variance cancellation.

Existing search dimensions are 16=6+5+5 and 43=15+14+14; ranks are independently established in third_moment_review. There is no need for an 8x8 residual: its role in the present trace numerator requires only a Rayleigh upper. Keep that seed's complete residual out of the initial job.

## Exact missing blocks

H'=Q+tA, t=g/2. B spans q0/q2; L,R have q4; M has q6. Set U=R+M, C=A_(q-2,q), Dq=Aqq, P=D4 R+CM, T=C†R+D6M. Accepted cached geometry supplies F=L*L, S=L*R, V=R*R, W=M*M, X=R*D4R, Y=R*CM, Z=M*D6M, and Gpair.

Only the U,U second-moment block requires new contractions:

 J_UU = 16V+36W + t[8X+10(Y+Y*)+12Z]
          + t²[D2 + P*P + T*T + CM*CM + M*[C,C†]M],
 D2=S* Gpair^(-1) S.

Save P*P, T*T, CM*CM and M*[C,C†]M separately, including signed commutator and its symmetry check. Each is d by d (d=5 or14). P*P, T*T, CM*CM are symmetric. Save the unsymmetrized commutator calculation too, and require exact symmetry. The complete q8 norm matrix is CM*CM plus the signed commutator; certify PSD, never discard its negative term.

All other J blocks follow from H'(B,L) and the cached first-moment geometry: their images are in span(B,L,U). Thus do not physically contract all 16 or43 image columns. Build the new d-column block, then assemble J exactly at any coupling. Output Q², QA+AQ and A² matrices to permit later exact coupling-polynomial evaluation. Existing single-vector residuals determine only one quadratic-form value each and do NOT determine this missing matrix.

## Coverage and implementation

Use one shared stream through ALL fixed-origin q4/q6 supports, not just M-active supports. Compute existing amplitude arrays once per support. Accumulate the matrix contractions instead of projecting immediately onto a chosen coefficient vector. The q8 term still uses exactly the accepted signed hard-core commutator on q6, scaled by N/6; CM norm uses q4 scaling N/4. Preserve checks on M-zero supports because T can be nonzero there.

4x4: 455 q4 and3003 q6 supports, full R cache1820*168=305760 bytes with current fixed D14 layout. 8x4:4495 q4 and169911 q6; R cache35960*168=6041280 bytes. No q6 physical-state cache, no q8 support enumeration. 8x8 would require39711 q4 and7028847 q6 plus106743168-byte R cache; defer it.

Matrix storage is tiny: five d² int128 accumulators require15680 bytes at d14 (plus GMP serialization). Full 43² matrices of large rationals remain small compared with the R cache. Suggested producer cap100MiB initially; audit may have different implementation costs. Exact amplitude/accumulator overflow bounds must be re-established for matrix accumulation, with checked addition; reuse of a scalar bound without proof is insufficient.

## Operation and time model, not a measured promise

For q6, m=15 matching channels. Compute K=Gram*V then V* K: at most m²d+md² multiply-adds per d-column bilinear contraction. At d14 this is6090, versus225 for a scalar norm. There are two q6 matrix terms (T norm and M/commutator bilinear): about12180 operations per support, at most2.070 billion dense scalar multiply-adds across169911 supports. Symmetry/sparsity reduces this, while large-integer overhead may increase cost. Current scalar code does three225-operation q6 bilinears per support, so dense inner-product work is about18.05 times current scalar; geometry generation is shared rather than repeated.

Existing measured complete scalar runs are about.14 seconds4x4 and4.75 seconds8x4 on CPU3. An 8x4 matrix projection of roughly85 seconds assumes inner-product scaling dominates; this is an estimate, not an accepted resource gate. Propose first a 5 CPU-second bounded representative microbenchmark after local fixtures, then authorize the full pass only if conservative projection is below300 CPU seconds and100MiB. Hard stop/checkpoint at600 CPU seconds/256MiB if that larger cap is explicitly authorized. The 8x8 all-q6 count is41.37 times8x4; its full matrix pass is not justified by this estimate.

Repeated 14-direction plus105 pair-polarization scalar residual runs would revisit all supports119 times, roughly565 seconds from the old4.75-second run before overhead; a 105-witness variant uses diagonals plus off-diagonal sums totaling105 runs, roughly499 seconds. One shared matrix pass avoids repeated geometry generation and gives every future trial/coupling evaluation. The exact number for a symmetric14x14 matrix is14+91=105 scalar quadratic forms.

## Residual-aware optimization and certification

At a fixed valid even-sector cutoff a, test the pencil

 M(ell)=J-(a+ell)K+a*ell*G.

An exact rational vector c with c*M(ell)*c<0 proves E0>ell once the sector has at most one level below a. Indeed if E0<=ell<a and every other level>=a, every eigenvalue of (H'-a)(H'-ell) is nonnegative, a contradiction. Equivalently, for rho<a, this is the strict Temple inequality var<(rho-ell)(a-rho). Use floating generalized eigensolvers only to propose c and ell; certify the final rational quadratic form exactly. An exact PSD/positive-LDL pencil at a specified ell can establish a limitation of THIS finite-dimensional Temple test, not of every bootstrap.

Check uniqueness separately with a physical Rayleigh below the full-Hilbert first-excited reference r1. For a=r2, retain and recheck all3N odd witnesses below r2 and the accepted full reference count. At g=.12 the bosonic stability condition g<1/4 holds, but odd-band residual denominators, mode endpoints, omitted tails and all trace/continuation inequalities must be freshly checked. The accepted short bridge now covers L2..7 through.1528; this removes only that particular obstruction.

No proposed matrix pass, pencil optimization or higher-coupling all-size certificate has been run in this package.
