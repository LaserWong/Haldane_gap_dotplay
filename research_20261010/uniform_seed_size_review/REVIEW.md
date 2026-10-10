# Independent review: uniform spin-one seed-size obstruction

Updated 2026-10-10 17:14 EDT (America/New_York, UTC−4) / 21:14 UTC.

## Verdict

**PASS, with the explicit fixed-recipe scope below.** Independent integer Hamiltonian actions, trial orthogonality, D26 matrix reconstruction and contractions through length 24, directed exponential bounds, and exhaustive permitted delayed conversions all pass. No numerical eigensolver or many-body spectrum is a verification premise.

The frozen producer is `../uniform_seed_size_diagnostics`. Its manifest SHA-256 is `a67ebcf6d8ec1aca3a0fee0013573492b0ad8237d59ebe7695040e16deacdf6b`; all 28 entries match. The previously accepted nonperturbative-MPS review (22 entries) and joint-ratio lemma review (13 entries) also match their manifests. This audit writes only in its own directory. It changes no producer, frozen input, root index or GitHub file. The extracted shared workspace has no Git metadata.

### Exactly what is accepted

For the periodic unit-coupling spin-one Heisenberg chain at even denominator lengths n=6,8,10,12, fix the archived D26 MPS at numerator length 2n, retain exactly its single Rayleigh contribution exp(−2 beta R), and use the specified G-based time-first initialization.

- At n=6 and n=8, every beta≥0 is excluded for immediate canonical conversion and for every legal completed time-first-cycle delay followed by the specified joint-aware conversion. The only positive conversion opportunities are delay 0 at n=6, and delays 0 or 1 at n=8. Each fails in the first converted canonical cycle. The old joint K is correctly discarded after that cycle.
- At n=10, the attainable certificate input J_lower is strictly below 3/25 for every beta≥0. At n=12, it is strictly below 19/100. These upper caps use four orthogonal denominator witnesses. Keeping only two gives J_lower<3/10 at either size, already making the first G update negative.
- These obstructions hold for every valid choice of upper denominator traces, including exact traces, while the lower numerator is fixed to this recipe.

### What is not accepted or claimed

These are **upper bounds on the lower ratios this certificate can produce**, not upper bounds on actual physical purities. They prove no physical gap upper/lower bound and do not exclude all MPS states or methods. They do not cover richer numerator contributions, a different MPS, other purification inequalities, independent new information at later bases, arbitrary adaptive direction switching, larger seeds, or untested smaller sizes. No successful minimum seed has been found. “Minimum” can only refer to the explicitly tested family and fixed recipe; n=14 is an untested next size, not a certified minimum or a certified success.

## 1. Physical normalization and trace direction

Use H_n=sum_j S_j·S_(j+1 mod n), with n microscopic spins and no extensive shift. In the orthonormal spin-z product basis, each local bond has diagonal m_j m_(j+1) and off-diagonal coefficient 1 on each allowed opposite ladder step. The latter follows from (1/2) sqrt(2) sqrt(2)=1. The implementation includes every periodic bond. An extensive shift c n cancels from the ratios and delta below; several exact rational shifts are explicitly tested.

Write Z_n(beta)=Tr exp(−beta H_n). Let R be the total, not per-site, Rayleigh energy of the fixed numerator state at length 2n. Its contribution satisfies exp(−2 beta R)≤Z_(2n)(2 beta). The recipe is

    J_lower = exp(−2 beta R)/U0^4,
    C_lower = exp(−2 beta R)/U1^2,
    U0≥Z_n(beta), U1≥Z_n(2 beta).

For any orthonormal trial family with exact expectations alpha_i, scalar Jensen applied separately to each spectral measure gives

    Z_n(beta) ≥ sum_i exp(−beta alpha_i).

The sum is valid because the trial vectors are orthogonal, not because their trial energies differ. No trial vector need be an eigenvector. Since every bond has trace zero, Tr H_n=0 and Z_n(beta)≥3^n. This trace is independently checked in the entire physical basis through n=12.

For alpha_0 the first trial energy, set delta=R−2 alpha_0>0 and g_i=alpha_i−alpha_0>0 for i>0. Then the **chosen lower recipe** obeys

    J_lower ≤ exp(−2 beta delta)/(1+sum_(i>0) exp(−beta g_i))^4,
    C_lower ≤ exp(−2 beta delta)/(1+sum_(i>0) exp(−2 beta g_i))^2.

Both follow by lower-bounding a denominator already bounded above by U0 or U1. The numerator is not replaced by a larger physical trace. The negative regression example uses rational thermal weights to show why the same argument cannot upper-bound actual physical purity: a trial numerator 1/4 and true numerator 5/4 over denominator 2^4 give 1/64 versus 5/64.

The optional complement refinement is also valid. Complete the r orthonormal trials to a full orthonormal basis. The complement's diagonal-energy sum is −sum_i alpha_i, whether or not that subspace is invariant under H. Jensen over its D−r entries adds

    (D−r) exp(beta sum_i alpha_i/(D−r)),  D=3^n.

The six reported samples are independently enclosed. They are diagnostic refinements, not the premise of the all-beta exclusion.

## 2. Trial-vector reconstruction and orthogonality

`independent_trials.py` does not import NumPy, SciPy or producer functions. It constructs each total-Sz basis recursively in ascending base-three code order and applies the complete physical Hamiltonian with arbitrary-precision Python integer dictionaries. It independently matches every coefficient hash, full H-action hash, integer norm, energy form and reduced rational Rayleigh quotient in the frozen producer. Nonzero output outside the original nonzero support is retained.

For n=10/12 the first saved vector has Sz=0 and translation eigenvalue +1; the second has Sz=1 and eigenvalue −1. Both translation identities are checked at every basis position. Global spin flip gives the Sz=−1 vector. The exact operator sum_j S_j^−/sqrt(2) gives another Sz=0 vector with translation eigenvalue −1. All four norms are positive. The full integer Gram matrix is diagonal. Different Sz sectors are disjoint; the two Sz=0 vectors are orthogonal both by opposite momentum and by directly computed zero inner product.

The spin-flip and lowering constructions are additionally checked against H action: H Fv=F Hv and H Lv=L Hv as exact sparse vectors. The lowered Rayleigh quotient is recomputed, and is slightly different from its parent in both sizes. No exact spin-multiplet or equal-energy assumption is used. A regression rejects substituting the parent's Rayleigh energy for the lowered one.

Relevant dimensions remain distinct:

- n=10: complete physical dimension 59,049; Sz=0 dimension 8,953; Sz=1 dimension 8,350.
- n=12: complete physical dimension 531,441; Sz=0 dimension 73,789; Sz=1 dimension 69,576.
- There are four retained orthogonal denominator trials generated from two stored integer vectors. Two trials suffice for the weaker obstruction.
- Numerator MPS bond dimension is 26, and retained numerator span dimension is one. At length 24 the full physical dimension is 3^24=282,429,536,481; neither its matrix nor its full coefficient vector is formed.

The complete support counts, Gram matrices and exact arithmetic are in `independent_trials.json`.

## 3. Independent D26 source contraction

`independent_d26.py` reconstructs the three 26×26 matrices from the archived scalar parameters, rather than importing the producer builder. It builds the physical two-site spin-one interaction explicitly. It then constructs each transfer-block entry directly:

    T_(i,j),(k,l) = sum_s A_s(i,k) A_s(j,l),
    O_(i,j),(k,l) = sum_(s,t,u,v) h_(s,t),(u,v)
                    (A_s A_t)(i,k) (A_u A_v)(j,l).

Auxiliary magnetic-difference conservation is checked. The block dimensions are 1,8,32,80,136,162,136,80,32,8,1, summing to 676=26^2. The resulting block bytes match the archived block file exactly. Direct amplitude expansion at lengths 2 and 3 independently checks physical norm and total Heisenberg energy; length 2 includes both periodic parallel bonds. The original manuscript PDF is absent, so matching these archived parameters to that unavailable text is not asserted.

The independent C++ GMP engine advances sequentially through T^1,...,T^24. It does not use the producer's repeated-squaring schedule. It obtains

    U_L=Tr(T^(L−2) O), V_L=Tr(T^L), R=L U_L/V_L.

All eight integers U_L,V_L for L=12,16,20,24 match the frozen producer byte-for-byte. The R−2 alpha_0 differences are positive rational numbers, displayed as:

- n=6: 0.365339682084205
- n=8: 0.22713595626665797
- n=10: 0.14800926169918177
- n=12: 0.09857253720308078

The exact values are in `independent_scalar.json`; display decimals are never used for decisions.

## 4. All-beta n=6/8 exclusion with joint-aware conversion

The dimension bound increases with beta because R<0, while exp(−2 beta delta) decreases. Splits at beta=3/4 for n=6 and beta=31/40 for n=8 give global strict caps J_lower<29/50 and J_lower<71/100.

For beta≤1/2, the dimension term yields J_lower<2/5, so G(J_lower)<G(2/5)=−1/8. For beta≥1/2, the one-trial bound gives C_lower≤exp(−delta)<4/5. With G(z)=1−(1−z)^2/(2 z^2), its derivative (1−z)/z^3 is nonnegative on (0,1]. Thus the optimistic positive staircase is bounded above by

    a_bar=G(J_cap), b_bar=G((4/5)^2 a_bar).

All subsequent arithmetic rounds upward, appropriate for an impossibility certificate. If any true certified endpoint becomes nonpositive earlier, that path already fails. Otherwise monotonicity places it below the simulated optimistic endpoint.

At each completed time-first cycle, the staircase base is (2 n·2^r, 2 beta·2^r). The allowed conversion at that same base is

    s=a sqrt(b), t=a^2 b, K=a^2 b,
    s_new=G(max(s^2 t,K)),
    t_new=G(max(t,K)^2 s_new).

This is the accepted joint-aware rule, not the old product-only replay. The original K is dropped at the newly doubled base. Later cycles use only the new component product unless a new independently justified K is supplied; such added information is outside this recipe.

The complete exact delay enumeration is:

- n=6, r=0: the first canonical spatial output is at most −6.5834967580. An additional time-first cycle itself fails in its first direction, so there is no r≥1 opportunity.
- n=8, r=0: the first canonical thermal output is at most −1.0437586755.
- n=8, r=1: the first canonical spatial output is at most −3.6588800792. The next time-first cycle fails before another completed-cycle conversion can occur.

Every preceding positive pair has at least one optimistic component below 99/100, so it has not already entered the inherited common small-defect trigger region. These finite witnesses therefore exhaust all legal completed-cycle delays, not an arbitrary finite search. Every argument and upward endpoint is saved in `independent_scalar.json`.

## 5. All-beta n=10/12 hot, closed-box and cold proof

The exact trial gaps g_i and delta are positive. The covering consists of:

1. beta∈[0,1/2]: J_lower≤exp(−R)/3^(4n).
2. Each of the 38 closed boxes [i/4,(i+1)/4], i=2,...,39: for l≤beta≤h,

       J_lower ≤ exp(−2 l delta)/(1+sum_(i>0) exp(−h g_i))^4.

3. beta≥10: J_lower≤exp(−20 delta).

The direction of both endpoint choices is checked: the numerator decreases with beta, while replacing each denominator exponential by its value at the right endpoint makes the denominator smaller. Independent arithmetic encloses numerator exponentials above and denominator exponentials below. Closed-box boundary equalities and complete coverage of [1/2,10] are tested explicitly.

At n=10, every bound is below 3/25; the largest warm bound is approximately 0.1138414784449191. At n=12, every bound is below 19/100; the largest warm bound is approximately 0.1801389902342928. Both cap values have negative G, making every later recursion irrelevant.

Using only the first two orthogonal trials, all hot/box/cold bounds are below 3/10. The largest warm bounds are approximately 0.2115271998109677 and 0.28175830277215524. Consequently the simpler two-vector version already proves failure before any spin-flip/lowering-derived states are needed.

This is an exact half-line covering. It is not a beta grid scan, and no unbounded cold range is omitted.

## 6. Independent arithmetic, regressions and resources

The scalar review uses decimal directed arithmetic, unlike the producer's binary 160-bit grid. It reduces a positive exponent to [0,1], encloses it on a 10^40 grid, adds 96 outward-rounded Taylor terms, and uses the positive geometric tail

    next_term/(1−x_upper/98).

It then squares outward to recover the original argument. Negative exponents use outward reciprocals. Recurrences round upward to a 10^26 grid; square-root upper endpoints are checked by exact squaring. Fraction comparisons decide every inequality.

Regressions verify exponent reciprocals, extensive-shift cancellation, physical/recipe ratio distinction, complete closed-box coverage and all allowable delay enumeration. Source inspection confirms old-K disposal; all tested converted paths actually fail in their first cycle, so none relies on joint information at a later base. Negative tests reject duplicate “orthogonal” trials, missing boxes, per-site/total-energy confusion, and unjustified equality of lowered energies. The separate analytic n=14 sector/entry/storage counts match exactly; the producer's future CPU and memory ranges remain unverified forecasts. No n=14 support or trial proposal was generated.

Run `bash REPRODUCE.sh` in a disposable copy of this review placed alongside the producer and previous review directories. Replay writes only local review results, so do not run it in a sealed directory if byte-identical timing metadata is required. It pins one permitted CPU, caps address space at 1 GiB, and runs all stages sequentially. Python, g++, and GMP are required; no NumPy, SciPy or eigensolver is required by the independent audit. Recorded resource details are in `RESOURCES.json`.

## 7. Provenance and status

`INPUT_SHA256.json` identifies every consumed frozen input and accepted-review dependency. `provenance_results.json` records matching manifests. `CLAIM_VERDICTS.json` separates accepted statements, inherited transfer premises and rejected overextensions. `MANIFEST_SHA256.json` plus `SEAL.json` freeze this independent review.

The inherited even-base transfer representation and scalar G purification theorem were read in the accepted MPS and joint-ratio reviews. This audit does not recertify the original upper seam/sector moments, any pre-existing Haldane gap, or an unseen original manuscript. It verifies the stated recipe obstruction directly and preserves those premise boundaries.
