# What could remove the deficit?

Analytical assessment only. No additional numerical search or physical computation followed the resource-limit finding. The new interval-localizer argument below is written analytically and has not been independently machine-checked.

## 1. Joint extremal positive-moment optimization

Replacing separate support and polynomial bounds by one convex positive-measure optimization is worth distinguishing from enforcing the entire integer-multiplicity spectrum. They are not equivalent.

The existing exact diagnostic removes one unit J atom

    t=20063/20000=1.00315

from the MIDPOINT m2,...,m6 enclosure data. Its residual3×3 Hankel matrix is strictly positive definite, with exact LDL pivots recorded in diagnostics.json; the last pivot is about4.5091e−6. The2×2 positive-half-line localizer built from residual m3,m4,m5 is also strictly positive definite. Thus no degree-two square filter or degree-one x-weighted square filter can exclude this atom for those midpoint data.

One can also impose the known compact support[0,U], U=1.003155126. Let r_j=m_(2+j)−t^(2+j), j=0,...,4. The compact-interval localizer is

    L=[[U r1−r2, U r2−r3], [U r2−r3, U r3−r4]].

The exact definitions imply the conservative rational brackets

    2.423<r1<2.424, .529<r2<.531,
    .154<r3<.155, .046<r4<.047,
    1.003<U<1.004.

Consequently L00>1.89, L11>.107 and 0<L01<.38, giving det L>1.89·.107−.38²=.05783>0. Together with the exact positive3×3 Hankel matrix, the standard univariate degree-four interval moment criterion gives a nonnegative weighted residual measure on[0,U]. One way to justify that criterion is the quartic representation p=sum(q2²)+x(U−x)sum(q1²) for polynomials nonnegative on[0,U], followed by separation from the compact moment-curve cone.

This positive weighted relaxation therefore permits an actual unit atom at t plus a residual weighted measure matching the five J midpoint moments. The atom alone contributes

    t^34 ≥1+34(.00315)+561(.00315)^2
          =1.1126665225 >1.0944628815077482.

So the sector-J continuous positive-moment problem, even after adding a forced unit leading atom, cannot deliver the displayed denominator target. Merely choosing a better quartic envelope or solving that same relaxation jointly will not bridge it. Full unit multiplicity of EVERY remaining eigenvalue is stronger and is not satisfied or disproved by this weighted witness. Likewise the residual measure may not arise from the Heisenberg history kernel. This is not an integer-spectrum or physical no-go theorem.

This argument concerns the J sector's midpoint box. It does not separately prove infeasibility of every optimization retaining the original shared I/P interval correlations across J and N; a fully correlated witness was not constructed. Nor does it exclude a different way to obtain S and T simultaneously, different purity recurrences, or a different temperature. Those are genuinely stronger questions.

## 2. Does A A* or reflection positivity supply another constraint?

Abstract factorization as A A* supplies positivity and trace class. Every positive trace-class spectrum admits such a factorization, so this fact by itself does not remove the high-atom positive-moment witness. Equivariance supplies the positive character sectors already used. Simply restating reflection symmetry, the same scalar Hankel positivity, or pi rotation invariance is not additional spectral information.

The physical chronological kernel contains more structure than a generic positive operator. A new model-specific inequality, a mixed-boundary reflection-positive matrix, or extra symmetry-resolved trace observables might exploit that structure. Such a proposal must specify the new matrix entries or analytic inequality and demonstrate that they exclude the witness; one cannot count them as already present in the ten scalar I/P traces. Cross-temperature transfer spectra must not be identified: K_(2 beta) is not K_beta².

A second route is stronger integer-multiplicity constraints on all residual atoms. The one-unit-atom Hankel exclusion and dominant-atom forcing used here do not solve this nonconvex integral-spectrum problem. No claim of its infeasibility is made.

## 3. What one additional even physical length would add

Physical L14 gives cell m7, separately in J and N if both I and P seams are computed. It adds a genuinely new shifted3×3 necessary matrix

    [[m3,m4,m5],[m4,m5,m6],[m5,m6,m7]].

After removing a proposed unit atom t, write r_j=m_(2+j)−t^(2+j). With A=[[r1,r2],[r2,r3]] and v=(r3,r4), positivity requires

    m7−t^7≥v^T A^(−1)v

when A>0. Thus an upper bound for m7 below t^7+v^T A^(−1)v would exclude that high atom. Compact-support localizers provide companion constraints, and degree-five long-moment envelopes become available. This is a precise sensitivity test to carry out BEFORE buying a physical calculation.

However, m7 does not create the full4×4 Hankel matrix from m2 onward; that needs m8, hence physical L16 as well. Neither the value nor achievable interval width of alternating m7 is known here. L14 may or may not repair the seed, and L16 must not be smuggled in as an assumed cheap follow-up.

The direct full Hilbert dimension rises from3^12=531441 to3^14=4782969 and3^16=43046721. A brute full-trace method that applies a polynomial to every basis vector has roughly quadratic dimension cost before symmetry reductions, so the respective raw work factors are about81 and6561, before length, precision, and symmetry-loss effects. This is a complexity warning, not a measured runtime forecast. A period-two chain retains fewer translations than the uniform chain. Actual sector sparsity, usable symmetries, matrix-free storage and exact-arithmetic sizes must be benchmarked; no affordable L14/L16 campaign is established.

## 4. Better trial numerator is distinct from a better denominator

The thermal endpoint is

    T≥exp(−2 beta R_trial)/Q34².

At fixed current Q34, a better physical68 trial would suffice for T≥.835 if

    R_new≤−log[(167/200) Q34²]/(2 beta).

This is roughly−.0014 in TOTAL shifted energy, compared with the current−.00000832217860677. The exact formula, not that rough display, defines the target. A lower R is a better variational state; it need not alter any heat moment or denominator upper bound. A stronger numerator also improves the forced leading-atom lower bound, so holding S fixed is conservative.

There is no evidence here that D26 optimization, a larger trial span, or even the true ground energy achieves that target for the chosen shift. The Rayleigh principle supplies upper bounds on ground energy, not a guarantee of how much an optimizer can gain. Conversely, failure of the present fixed MPS anchor does not rule out a stronger numerator. A period-two MPS at g=.9 is a NEW trial and must be physically contracted at its own lengths, with exact rational tensor/energy validation; none of the uniform anchors can be relabeled.

## Recommended order

First seek a stronger scalar theorem or a demonstrated numerator improvement at the uniform feasibility point. Quantify the required extra-moment or numerator information before launching thermal work. A cheap g=.9 MPS optimization alone can be an exploratory variational pilot if separately approved, but cannot establish that the ten-trace bootstrap will close. The expensive heat pilot remains gated on an actual nonperturbative seed design with a credible success margin.

## 5. Is an energy lower bound already strong enough to rule out a numerator rescue?

The consumed independent anchors certify norm and mean energy, not H² or a Temple-type lower energy bound. No sufficiently sharp total ground-energy lower bound was found in the inspected anchor proof. The denominator itself does imply

    E0_shifted≥−log(Q34)/beta,
    exp(−2 beta E0_shifted)≤Q34².

This only caps the best possible numerator enough to give T≤1; it does not exclude the target T=.835. A genuine lower energy bound E_lower greater than

    −log[(167/200)Q34²]/(2 beta)

would rule out an MPS-only or any trial-only repair while Q34 is fixed. That comparison is the correct future gate. Neither a small variational energy nor the already-certified positive gap alone supplies this missing energy lower bound. A certified variance plus spectral separation might provide one, but would be additional information and is not computed here.

Technical detail for the relaxation witness: the residual measure above represents moments of the x²-weighted spectral measure. Strict positive definiteness persists for a sufficiently small inward movement of the support endpoints, so the representing measure can be chosen inside[epsilon,U−epsilon] with epsilon>0. Dividing its atom weights by x² then produces an ordinary nonnegative weighted spectral measure with the requested m2,...,m6. No positive weighted mass at x=0 is needed. The resulting weights are not asserted to be integers.
