# A 58-dimensional residual extension and conditional endpoints

2026-10-10 21:56 EDT / 2026-10-11 01:56 UTC. The cached algebra is complete, subject to the pending independent audit of the full physical row. Resource accounting remains unresolved as described below. This calculation changed no production file and ran neither a physical contraction nor the inner production CLI.

## Exact matrix checks

The new production row was appended to the accepted 57D G/H/H² polynomial, producing `complete_58d_polynomial.json`. The old 57D principal blocks agree entry-by-entry for all polynomial coefficients. The old 43D Gram and complete H² compressions also agree exactly, using each former U_i=R_i+M_i.

GMP rational LDL proves the following matrix properties.
- Gram rank 58, positive definite.
- A² positive definite.
- Complete 116-dimensional operator Gram [[G,A],[A,A²]] positive semidefinite, rank 87.
- Complete H² positive definite at g=.1085 and .11.

Q preserves each trial column's occupation (0,2,4,6). Consequently the complete [[G,H],[H,H²]] moment block at either nonzero coupling is an invertible congruence of the certified operator Gram, using [[I,Q],[0,gI/2]]. This is a full physical-image Gram check, not a projected-square substitution. Exact occupation identities were checked against every entry.

## Conditional endpoint results

Floating eigensolvers only proposed coefficient vectors. Both energy-minimizing and Temple-pencil proposals were rationalized with a common 2^96 scale, needed to retain the very small coefficient multiplying the large raw integer T. Norms, moments, variances, directed cutoffs, global-r1 margins and negative Temple-pencil expectations were recomputed with exact fractions.

- g=.1085: ground lower endpoint −.2997031216301698. The gain over the reoptimized 57D endpoint is 5.7748319243e−6. Ground-width proxy improves from .0004129152177712 to .0004035914963199.
- g=.11: ground lower endpoint −.30833747799084693. The gain is 6.4385719176e−6. Width improves from .0004622743275503 to .0004518496143935.

For each point, the actual new rational ground witness was combined with the cached optimized 4×4 denominator, 64-rung numerator, complete odd-band counting and tail bounds. The tested beta grid 7..14 in steps .05 produced no successful all-size scalar certificate at either point. Saved exact diagnostics are in `checkpoint.json`/`result.json`. This is failure of these vectors and the specified finite temperature grid, not a universal no-go.

Both previously selected g=.11 sufficient targets (beta=47/5 and 10) have positive-definite 58D Temple pencils at the fixed even-sector r2 cutoff. Near-root rational targets at both couplings are also positive definite. All exact pivots and target values are saved. These are scoped conditional exclusions inside this trial space/cutoff, not obstructions to every bootstrap or ansatz.

## Computation and resource caveat

The initial Python pass retained all merged matrices, rational witnesses and scalar outcomes before starting exact LDL. The LDL batch hit its 15-second wall timeout after six complete matrix jobs. Its completed output was preserved. Only the remaining three selected-target jobs were subsequently evaluated. All nine exact LDL results are now in `ldl_complete_results.json`. The incomplete first stream and recovery evidence remain intact.

The task requested at most 60 total CPU seconds, 256 MiB, CPU3, and BLAS1. The configured caps were 5 seconds for compilation, 45 for the parent, 10 for the initial LDL child, and 25 for the second LDL child. Parent CPU at the checkpoint was 5.9911 seconds. However the second child's RUSAGE_CHILDREN report was 33.13448 CPU seconds despite the 25-second hard cap setting. The initial child's actual CPU and final parent CPU were not retained. This discrepancy prevents a verified whole-task 60-second claim. Numerical work stopped when the discrepancy was observed and was reported as an unresolved accounting discrepancy. No more optimization or LDL work is authorized by this artifact. The source shows the requested limits. The result does not claim that their enforcement was independently verified.

The full production campaign remains separately sealed and its reviewed 360-CPU-second/100-MiB accounting is unchanged. This resource caveat concerns only the subsequent cached-algebra task. Scientific matrix/rational outputs are retained for independent review and must not be promoted to new physical claims before that review.
