# Independent review of the uniform periodic spin one proof guide

Review date: 2026-10-11 03:14 UTC.

## Conclusion

ACCEPTED. The final guide is pinned to manifest SHA-256 `78514331ec4e434bc633dc2c16520e371bace16e1559e32520aa08ceb095dfd1`. All 11 guide members, 66 consumed-source pins, 15 complete dependency manifests, six original source Git blobs, and the extracted fields were verified. The inspected formulas and fresh exact scalar checks support the stated finite-volume theorem: the unit-bilinear, untwisted periodic spin-one chain has a unique ground state and gap at least 31/1250 for every integer L >= 2. The L = 2 periodic Hamiltonian counts the same bond twice. This review does not establish a new physical input, a new gap theorem, or uniqueness of infinite-volume ground states.

The accepted theorem dependency is `uniform_gap_0248_all_sizes_review`, manifest SHA-256 `5407745b521a61a310d89857da94c14a73fcc2093a80d467dc8f72e9fd31deaf`. The stronger tail starts from canonical initialization n = 34. The separate smaller successful n = 30 initialization has the weaker bound 179/10000. Neither all-size coverage onset 2 nor the n = 30 result changes the initialization of the stronger proof.

This is future Stage20 material. It does not modify or block the already frozen Stage19 package.

## Findings and their resolution

1. No mathematical defect was found in the stated theorem or its logical chain. In addition to reading the guide, this review inspected the original model, transfer, thermal, initialization, and MPS source formulas and the relevant physical/scalar reviewer implementations.
2. The capped-mass lemma should explicitly require m >= 0 and h > 0 before using floor(m/h). All actual applications satisfy these conditions. The frozen guide now states both conditions explicitly. This is a domain clarification, not a defect in an applied bound.
3. The guide's initial self-check omitted an explicit equality joining its first saved n34 state to its certified seed. The underlying data has the correct equality, which this review independently checks. The frozen checker now includes the explicit first-state equality.
4. The initial guide self-check records 30.21035921 process CPU seconds despite a self-imposed 30-second RLIMIT_CPU. It must not be described as meeting a strict measured 30-second budget. The original script/output are retained unchanged in the guide history. The final documented 60-second replay records 25.746380744 CPU seconds and 19056 KiB peak RSS. The review inspected its corrected source and preserved records, and performed its own separate exact scalar replay. This new self-check record is separate from the historical direct25 resource exception.

## Audit of the logical chain

### Model, trace identity, and signed sectors

The guide's spin commutator, Casimir, unit bilinear coupling, periodic seam, and scalar shift agree with original `model.tex`. The two-site eigenvalues are -2, -1, and 1. The open-triad weighted-row argument proves the stated lower energy bound. Its application to seam-crossing open triads requires only local unitary equivalence and does not assume even ring length.

Original `transfer.tex` gives the self-adjoint Hilbert–Schmidt history transfer and the physical trace identity for every integer L >= 4. The chronological product is not reversed when histories are exchanged. Absolute convergence justifies regrouping. The signed rotation representation supplies the I/P seam traces. Odd untwisted lengths remain the same physical model, without a staggered gauge or hidden twist. The guide correctly treats L = 2 and 3 separately.

The D2 character decomposition gives J = (ZI + 3 ZP)/4 and N = (ZI - ZP)/4. Every occurrence has unit multiplicity in its sector and N occurs three times in the full spectrum. The invariant J sector is not assumed one-dimensional. All signed moments are powers of lambda, including odd orders. This review recalculated all 18 sector intervals from physical inputs, with subtraction reversing the P endpoints. The N upper endpoints at orders 5, 7, 9, and 11 are strictly negative.

### Full physical thermal errors

The inspected source uses D = 32 I - 3 L I - 2 H, R = D/32, and F = exp[98(R-I)] at beta = 49/4. The energy bound makes R a contraction for lengths 4 through 12. The integer Horner recursion uses mathematical floor, including negative coordinates. Conditioned Poisson truncation and normalization, 281 coefficient/coordinate rounding steps, and representative multiplicities are included in the error bound.

The row bound 76 and coordinate bound 2 times 2^55 fit signed 64-bit partial sums. Exact wide-integer and GMP accumulation are part of the previously accepted kernel evidence. The orbit argument preserves the full 3^L physical dimension, including negative-magnetization partners, stabilizers, and the signed translation restoring a pi seam on odd rings. Rounded columns are not falsely assumed equivariant.

This review recalculated every rational thermal interval directly from the accepted W integer, integer square root, Frobenius error bound, and Taylor exponential enclosure. All match the stored physical intervals and refined 10^-18 endpoint mapping. It did not recompute W or run a physical heat column. The original full physical review remains the source of matrix/checkpoint/kernel acceptance.

### Support filters, majorants, and countable spectra

Four exact square filters were recalculated. Their shifted polynomial coefficients are strictly positive on the complete exterior rays and their boundary margins are strictly positive. This proves exclusion on each whole ray, not only at an endpoint. The unit-atom interpretation is essential and is accurately stated.

All 26 long even-sector majorants and all 14 finite-prefix majorants were independently replayed. Each complete polynomial p(x) - x^(k-4) was converted to its full-degree Bernstein form over the complete signed support interval. Exact bisection certified every terminal leaf. Leaf counts, depths, and sign-directed moment sums match the accepted certificates. No floating search, grid, truncated eigenvalue rank, or division by x enters acceptance. Negative odd N sums remain negative.

The capped-mass argument is valid for a countable spectrum by finite-subfamily limits. Taking the minimum of separately proved packing and polynomial upper bounds is valid. The full trace retains J + 3 N. The guide correctly distinguishes numerical proposals and displays from these exact certificates.

### Physical MPS, total-energy convention, and Jensen

Original `trials.tex` and the inspected independent D26 rebuild define the same real integer site tensors and physical Heisenberg insertion. The norm is Tr(Atransfer^L). A one-bond insertion is Tr(Atransfer^(L-2) O), so the total physical numerator is L times that value. The newer H0 files already contain the total numerator. The correct shifted quotient is H0/N0 + aL, with no second factor L.

The own-length norm and energy integers at every direct size were checked as archived accepted data. The sign of the MPS68 shifted quotient is negative. The own-length MPS25 shifted quotient is positive. Its strictly subunit exponential numerator is retained and independently checked. A one-dimensional retained trial span, bond dimension 26, norm-transfer dimension 676, and physical dimension 3^L are not interchangeable.

Jensen, or the variational principle followed by positivity of the remaining Gibbs terms, provides the physical numerator lower bound. This requires no prior ground-state uniqueness and remains valid for positive trial energy. The proof obtains uniqueness only later from the full Gibbs purity.

### Purity and the n34 infinite tail

For a probability list, purity at least C > 1/2 forces the largest weight to exceed 1/2 and be unique. The ratio of any excited weight to the ground weight is at most (1-C)/C. The inequality C - upper_exp(beta delta)(1-C) > 0 therefore proves the gap and ground-state simplicity together. The rational endpoint in the theorem is conservative.

The n34 forcing inequality was recalculated with the certified twelfth mass and whole-sector bounds. It forces one positive J occurrence above ell, because ell exceeds the negative J cap and the entire N modulus cap. Removing its unit mass leaves less than ell^12, excluding another equally large occurrence. The resulting S34 and T68 lower bounds, their exact signs, and the initial saved state agree.

The exchange identity and purification inequality produce the staggered update Snew = G(S^2 T), Tnew = G(T^2 Snew). The new spatial endpoint is used in the second update. All ten saved states and windows were checked with directed roots and exponentials. Every window has a positive gap margin at 31/1250.

The integer-window argument is valid for signed spectra. Purity identifies a unique largest-modulus transfer eigenvalue. If its sign were negative, sufficiently large odd moments would be negative because the relative absolute tail tends to zero. This contradicts the positive physical trace at every odd length. Holder interpolation uses absolute eigenvalues between even endpoints. The resulting bound applies to every integer in each closed window without assuming gap monotonicity.

The small-defect inequalities hold on the full stated interval 0 < u <= 1/100. This review checked rational sufficient inequalities for both quadratic updates, the root/rho/d bounds, C >= 1-4u, and (1-C)/C <= 5u. The terminal state has n = 17408, beta = 6272, and 5u exp(beta delta) < 1. Analytic squaring then covers all later windows. This is an infinite continuation argument, not a finite numerical scan or continued fixed-precision iteration.

### The finite prefix and the special length 24

Spin addition independently gives representation multiplicities (1,1,1) at L = 2 and (1,3,2,1) at L = 3. With the doubled L2 bond, the spectra have exact gaps 2 and 1 and unique singlets.

Lengths 4 through 23 use their own physical MPS numerators and the untwisted thermal or signed-moment denominators. Length 25 and each length 26 through 33 likewise use an own-length numerator. For odd targets, the denominator may use Cauchy–Schwarz between the adjacent even physical trace bounds. It never substitutes a neighboring trial energy for the numerator.

Length 24 is different. Its accepted certificate is the even-parity inequality C24 <= S24 sqrt[T48/(1+rho^2)] and uses the negative-energy physical MPS48 anchor. This review reconstructed the 48-site shifted quotient, seed forcing, seed S/T bounds, and the saved C24 inequality. There is no own-length MPS24 numerator in this route and no claim of successful n24 infinite initialization.

All 30 exact purities at lengths 4 through 33 were rechecked against the stronger 31/1250 target. Thus the stronger claim does not merely reuse the text of a weaker 0.0023 conclusion. The sets {2,3}, [4,25], [26,33], and [34,infinity) cover all integers L >= 2. There is no missing odd length or junction.

### Original attribution and scope

The original introduction states (4/105) log(80/79) for every even L >= 60 and log(20)/784 for every even L >= 2304. The guide gives those formulas and scopes accurately. Original source Git-blob identities were checked. Independently computed rational logarithm enclosures support the displayed comparison ratios, about 51.7538176028648 and 6.49029960775952. These compare proved lower bounds, not physical gap values.

The original work already used the self-adjoint spatial transfer, symmetry sectors, certified thermal matrix polynomials, fixed D26 MPS family, two initializations including n36 at beta49/4, and coupled purity bootstrap. It had no full-exact-diagonalization premise. The guide credits those ingredients correctly and restricts its improvement claims to the reproduced inputs, stronger signed moments, smaller successful starts, all-integer interpolation, and complete finite prefix. It makes no minimum-seed, optimal-gap, or infinite-ground-state uniqueness claim.

## Executed checks and reproduction boundary

`check_exact.py` is a fresh standard-library scalar audit, with 60-second CPU and 256-MiB address-space limits. The successful run used 13.752261373 process CPU seconds and 18756 KiB peak RSS. It verifies seven complete accepted review manifests and their members, physical-to-moment conversion, four filters, 40 global majorants, all 30 finite purities, exact small-size representation counts, n34 seed/recurrence/windows/closure, and original comparison formulas. `CHECK_RESULTS.json` contains the exact results. `INPUT_SHA256.json` pins every consumed dependency.

`verify_guide_package.py` separately checks the final guide seal, all member identities, complete source-package manifests, original Git blobs, exact extracted data, the two code/prose corrections, and both preserved self-check histories. Its result is `GUIDE_PACKAGE_RESULTS.json`. No author self-check was rerun or overwritten by this review.

`check_edge_cases.py` supplies ten exact sanity/adversarial checks for positive odd trial energy, total-energy factor confusion, negative floor semantics, signed odd moments, multiplicity three, endpoint-only polynomial tests, n30/n34 distinction, staggered updating, coverage holes, and the special MPS48 route at L24. Its output is `EDGE_CASE_RESULTS.json`.

Two initial checker-development failures are retained as attempt1 logs. One was a mistaken JSON field name in this new review script. The other was a test assuming the new S endpoint is already larger at the very first iteration, which is not guaranteed. The latter fixture was replaced by an explicit high-purity rational separating example. Neither failure was in a scientific producer or accepted certificate. The final checkers and outputs pass.

No new physical MPS contraction, heat column, optimization campaign, or GitHub write was performed. No producer, root-status file, prior certificate, historical label, or seal was modified. The workspace is an exported tree without a local Git repository. Historical direct25 resource nonacceptance remains unchanged. Hashes verify byte identity and do not replace mathematical or physical validation.
