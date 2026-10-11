# Physical-input reproduction: independent proof and acceptance conditions

This proof applies to the16 completed physical cases at lengths4–11. The campaign terminated before the two length12 traces were complete; this is not an all18-input certificate. See OUTCOME_REVIEW.md for the frozen partial acceptance and failure analysis.

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

## Relation to scalar theorems

Only after all18 physical intervals are independently accepted can their role as inherited published thermal premises be replaced by local physical reproduction evidence in previously reviewed scalar theorems. This artifact certifies the inputs, not a new scalar optimization. The conditional .0046 all-L≥36 theorem and any separately reviewed signed-moment improvement retain their own analytic certificates and scopes. The72-site variational anchor is a separate already reconstructed input. No minimum-size claim follows from thermal reproduction.

## Resources and state

The campaign's engineering gate fixes one persistent state path,21600 aggregateCPU seconds, two single-core256MiB worker trees and wallstop2026-10-11T06:00:00Z. Reviewer checks are separate CPU5 read-only work under256MiB, with no changes to campaign files, ledger or source. Live reservations must not be mistaken for spent CPU. The final review will pin the terminal ledger and all consumed case evidence; no mutable in-progress observation will be called a completed campaign.
