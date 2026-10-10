# Independent complete residual: 8x4 at g=0.105

Updated 2026-10-10 19:04 EDT / 23:04 UTC.

## Accepted physical result

The ordinary periodic spin-1/2 bilayer at g=21/200, unit rung exchange and the accepted positive-neighbor bond convention has the following verified trial data:

- Geometry: 8x4 rungs, 64 physical spins, full Hilbert dimension 2^64
- Trial dimension: 43; one retained even ground contribution
- Complete variance: 0.0005240758184406096
- Certified shifted ground-energy lower bound: -0.2801177779610626
- Selected sufficient component target met: False

The exact fractions and every sector norm are in audit.json. This physical-input result alone is not an all-size gap certificate. Actual scalar use requires the separately checked complete heat traces, all finite windows and short-size bridges. In particular missing a nonsharp sufficient component target does not invalidate the physical lower endpoint.

## Independent contraction and normalization

The unchanged independently accepted exhaustive-support checker is pinned by source and binary hashes to bilayer_complete_residual_8x4_review. No producer residual code is executed. It enumerates every fixed-origin q4 and q6 support, independently constructs the matching-tensor Gram/bond forms, and retains each support even when the trial's q6 M amplitude vanishes. The positive norm on those M-zero supports is checked explicitly.

The graph and pair-orbit identifiers are independently rebuilt from the periodic coordinates and compared entry by entry to the entire geometry input. The checker uses all B,L,U coefficients, while the vacuum coefficient is retained in the separate q0/q2 assembly. No basis column is silently dropped.

At g=21/200 the exact integer action is T=400H'=400Q+21A. The audit requires these exact integers and verifies every coefficient-file entry against trial.json. Coefficients have absolute value at most 2^48. The prior checked conservative intermediate bound used coefficients up to 2^56 with action factors 40 and 2. The new products 400*2^48 and21*2^48 are respectively only10/256 and10.5/256 of those bounds. Geometry and tensor combinatorics are unchanged or smaller. Thus the previously established scalar integer bounds remain safe; final quadratic sums use arbitrary precision.

The q8 norm uses the exact identity ||C_dagger M||^2=||CM||^2+<M,[C,C_dagger]M>. The independently implemented commutator expectation includes signed local cap and overlapping-bond terms. Neither negative contributions nor cross terms are removed. q8 physical configurations are not enumerated. Every independent q4, q6, CM, commutator, auxiliary and q8 norm matches the frozen producer integer exactly.

## Complete physical assembly and Temple validity

The reviewer reconstructs the fixed-basis Gram and affine H' matrices from accepted independently checked geometry at formal g=0 and1. Those formal points extract affine coefficients; no stability inequality is applied there. The exact trial norm and Rayleigh coefficients agree with the saved vector. All q0 and q2 image norms are evaluated through the complete invariant B-sector rows and their diagonal Gram. Symmetry ensures this B block spans the full q0/q2 image of the invariant singlet trial.

Orthogonality of triplet-number sectors gives

 <H'^2> = (N0+N2+N4+N6+21^2 N8_creation)/(400^2 ||psi||^2).

Subtracting the exact Rayleigh square gives the complete positive variance. This is not a projected second moment. Its q8 contribution is essential.

The stable oscillator reference at this physical g gives r1 and r2 with directed rational square roots. The trial mean is strictly below r1, proving a unique global ground state. The already independently checked fixed-z=.1 odd family supplies all 3N orthogonal odd directions below r2, and the complete counted reference puts level 3N+2 at or above r2. Together with the even ground this excludes a second low level in the even sector. Therefore the even-sector Temple denominator r2-rho is valid, yielding E0>=rho-variance/(r2-rho). The audit checks every odd upper endpoint remains below r2 and the full reference count reaches 4^N.

The target lower endpoint is matched to the independently accepted error-budget study, but not assumed true. Its variance budget is recalculated as (rho-L_target)(r2-rho). The comparison with the actual complete variance determines target_met. No selected target is substituted for an actual physical endpoint.

## Reusable complete polynomial

The audit also derives a complete fixed-vector coupling polynomial independently. It splits U=R(q4)+M(q6) into homogeneous columns, duplicating its coefficient in those two sectors. The resulting enlarged representation has 57 columns; this is only a bookkeeping representation of the same 43-dimensional trial vector, not an additional search.

The homogeneous Gram and first A matrices determine ||psi||^2, <Q>, <Q^2>, <A>, and <QA+AQ> exactly. The newly verified full second moment at nonzero g then determines the one remaining coefficient <A^2> from

 <H'(g)^2>=<Q^2>+(g/2)<QA+AQ>+(g^2/4)<A^2>.

Because H'(g)=Q+(g/2)A and the vector is fixed, this is an operator-polynomial identity for every real g, not interpolation from successful energy estimates. The exact affine Rayleigh and quadratic complete-variance coefficients are saved in audit.json.polynomial. The covariance inequalities v0>=0, v2>=0 and 4v0v2-v1^2>=0 are checked. Any later interval result must still certify its own physical cutoffs, thermal bounds, interior inequalities and all-size continuation.

## Resources, provenance and reproduction

The independent support replay took 13.986 CPU seconds and peak RSS 13824KiB. Assembly is separately measured in audit.json. CPU 4, 40 CPU seconds and 250 MiB address space are enforced for each support run. The higher memory ceiling follows the parent's explicit review allowance; it is not inferred from cache size. No resource limit was exceeded.

REPRODUCE.sh verifies every seal, rebuilds the pinned independent checker in a fresh directory under the same resource caps, reruns its full support enumeration, reassembles all exact outputs and compares the substantive result. Previous analytic/physical fixtures belong to the pinned unchanged checker review. All new outputs stay in this separate review; producer, root and GitHub files are preserved.
