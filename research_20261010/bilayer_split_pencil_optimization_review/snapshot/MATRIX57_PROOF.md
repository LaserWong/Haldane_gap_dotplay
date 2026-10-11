# Independent complete57D8x4 split R/M second moment

Accepted scope: the complete physical Gram, first moment and second-moment coupling polynomials for B15,L14,R14,M14 on8x4. Trial dimension57, physical dimension4^32=2^64. Trial q<=6; full H' image q<=8. This matrix acceptance is not a ground-energy endpoint or an all-size gap certificate.

## Independent physical support pass

The exact reviewer checker is unchanged from the accepted21D4x4 split fixture and is pinned by that independent review's manifest. It is derived from the separately implemented matching-coordinate reviewer engine, not from producer code. Its local image arrays are contracted BEFORE combining R/M contributions. All4495 fixed-origin q4 and169911 fixed-origin q6 supports are processed with exact N/4 and N/6 scaling and divisibility checks.

Five oriented14x14 blocks are independently calculated:
 R4R4=(A44R)*(A44R), R4CM=(A44R)*CM,
 R6R6=(C†R)*(C†R), R6M6=(C†R)*A66M,
 M6M6=(A66M)*(A66M).
All980 entries match the frozen producer exactly. Both cross matrices are genuinely nonsymmetric and their orientations are retained; they are never symmetrized.

The same independent pass reproduces the previously accepted PP,TT,CMCM and raw signed COMM matrices entry by entry. It also reproduces the old TT-on-M-zero matrix on96705 q6 supports. Those supports cannot be dropped. Exact recombination verifies the old PP/TT matrices, but the independently evaluated oriented split entries provide the stronger check against opposing errors that would cancel on compression.

The complete q8 norm is CMCM+COMM, including negative local commutator terms. Its positivity is checked exactly. Since R is q4, H'R has no q8 component. Since M is q6, H'M does; all of it remains in the M,M block. No q8 trial direction or q10 image is introduced.

## Pure-Python exact complete matrix assembly

The reviewer independently reconstructs the rectangular8x4 positive-neighbor graph and pair-orbit classes. Physical q0/q2 action and pair Gram are rebuilt directly. Accepted independent F,S,V,W,X,Y,Z blocks supply the remaining G and A matrix elements. No producer assembly code is imported or executed. Exact positive pivots prove Gram rank57.

Every split basis vector is homogeneous in triplet number. Thus Q_ij=G_ij q_j, (Q²)_ij=q_i G_ij q_j and (QA+AQ)_ij=(q_i+q_j)A_ij. The complete A images of B,L have an explicit coordinate map W satisfying GW=A[:,B,L]. Their full A² rows are W*A. The new bottom blocks are
 A²_RR=S*Gpair^(-1)S+R4R4+R6R6,
 A²_RM=R4CM+R6M6,
 A²_MM=CMCM+M6M6+(CMCM+COMM).
The q2 inverse-Gram term uses the complete invariant singlet pair basis; it is not a projected omission. Hermitian transpose gives M,R.

Every entry of G, both H' coefficients Q,A/2 and all9747 entries of the three57x57 H'^2 coefficients Q²,(QA+AQ)/2,A²/4 matches the frozen producer export. The reviewer stores its independently reconstructed polynomials in audit.json, so later exact endpoint work need not rely on a producer-only copy.

The embedding cR=cM recovers the old43D basis. Independently reconstructed old G and both H coefficients agree under compression, and all three previously independently accepted complete H² coefficients agree entry by entry. This coefficientwise identity holds for all real g. It does not invoke oscillator stability at formal extraction points.

At the physical test coupling g=.105, exact elimination proves J>=0 and the FULL114x114 block Gram [[G,K],[K,J]]>=0. Since G is positive definite, this is equivalent to the complete residual Gram J-KG^(-1)K>=0. Individual squared-image blocks and complete q8 Gram are also PSD. These structural tests supplement the independently contracted cross entries; PSD/compression alone would not certify them.

## Safety, sector obligations and limitations

The exact same checked arithmetic guards and conservative128-bit bounds from the accepted independent full matrix checker apply. Splitting adds separate accumulators without enlarging any local contraction term. Local updates are overflow checked and bounded to32 bits; matrix products are promoted to128 bits and accumulator additions checked. The absolute-sum bound including commutator terms and translation scaling remains below2^112. Signed cancellation is never needed for arithmetic safety.

All57 basis vectors remain exact even SU(2) singlets, because the underlying pair/creation/preserving operations have those symmetries. A later negative complete pencil J-(a+ell)K+a ell G with a=r2 requires fresh global r1 ground identification and odd-band counting to justify r2 as the cutoff in the FULL untruncated even-singlet sector. r2 must not be called the full-Hilbert second eigenvalue. No such new-coupling endpoint or scalar continuation is certified by this matrix-only review.

## Resources and reproduction

An independent partial sample projected43.0seconds and was used only as a resource gate. The actual complete independent pass used35.52CPU seconds and13.4MiB peak RSS under90CPU seconds/100MiB. Pure-Python exact57D assembly used3.77seconds and16.1MiB, avoiding NumPy's virtual-memory mappings. No independent support pass outside the authorized full8x4 scope was launched.

REPRODUCE.sh validates immutable hashes, recompiles the pinned independent source under the separate512MiB compiler allowance, repeats one full support pass under90CPU seconds/100MiB, reruns complete exact assembly, and compares scientific output. Producer/root/GitHub files remain unchanged.
