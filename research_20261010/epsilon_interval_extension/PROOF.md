# Uniform perturbation intervals from fixed rational trial vectors

Updated 10 October 2026, 13:52 EDT / 17:52 UTC.

## Result and verification status

This directory contains exact-arithmetic candidate certificates for the periodic square spin-1/2 bilayer with unit rung exchange, fixed crossed exchange J=3/10, and straight exchange J+epsilon. Positive-direction periodic adjacency terms are retained separately when a direction has length two. Every claim below concerns square tori and every integer side L>=2.

The new covered closed intervals are

| epsilon interval | Fixed trial-vector epsilon | Uniform gap lower bound | Initial beta | Asymptotic entry side |
| --- | --- | --- | --- | --- |
| [0.00475,0.006] | 0.006 | 0.026872599723 | 30.5 | 16 |
| [0.006,0.0075] | 0.0075 | 0.009589950085 | 31.5 | 32 |
| [0.0075,0.008] | 0.008 | 0.007867831452 | 32 | 32 |
| [0.008,0.00825] | 0.008 | 0.005936012610 | 32.5 | 64 |
| [0.00825,0.0085] | 0.0085 | 0.001703099464 | 32.5 | 128 |
| [0.0085,0.00855] | 0.0085 | 0.000768515509 | 32.5 | 256 |

Every displayed decimal is truncated downward. Exact fractions and all finite-window bounds are stored in the JSON files. Together with the previously independently audited product-state interval [0,0.00475], these candidate certificates cover [0,0.00855] without a gap. The common lower bound is greater than 0.000768515509. Restricting to [0,0.0085] gives the stronger common lower bound 0.001703099464. The initial unsplit run separately covers [0.00475,0.0085] with common lower bound 0.000997569515.

These results have been checked by the producer using exact full-action coefficients, endpoint PSD tests, 128-bit directed heat bounds, distinct 192-bit scalar enclosures and exact finite-window interpolation. A separate independent audit of the new interval construction remains pending. Existing point audits alone do not establish these continuum statements.

## Fixed-vector polynomial certificate

For each seed geometry 2x2, 4x2 or 4x4, let H(epsilon)=H_FF+epsilon V. H_FF includes the rung terms. Choose one fixed, nonzero rational vector psi for the entire closed parameter interval I=[l,h]. The stored integer vector is expressed in an orthogonal rational rung basis with exact positive diagonal metric. No parameter-dependent eigensolver result enters the certificate.

Normalize psi only in the following scalar expressions. Its Rayleigh quotient is affine,

    rho(epsilon) = <psi,H_FF psi>/<psi,psi>
                 + epsilon <psi,V psi>/<psi,psi>.

The complete squared residual is

    R(epsilon) = ||H(epsilon)psi||^2/||psi||^2 - rho(epsilon)^2
               = c0 + c1 epsilon + c2 epsilon^2.

The coefficient c2 equals the variance of V in psi, so c2>=0. The code constructs H_FF psi and V psi on the entire union of reached configurations, including configurations outside the trial space. Exact metric contractions give all coefficients. The polynomial evaluated at the vector's original epsilon matches both the saved exact Rayleigh quotient and saved full residual. Thus R is convex and

    rho(epsilon) <= rho_max = max(rho(l),rho(h)),
    R(epsilon) <= R_max = max(R(l),R(h)).

The lower Rayleigh endpoint is not substituted into the thermal ground factor. Retaining the common affine energy shift avoids an artificial uncertainty proportional to the interval width.

## Uniform full-spectrum lower reference

For each geometry and interval choose fixed rational a>=0 and b>0. The exact 16-dimensional physical-spin matrix

    M(epsilon)=epsilon v_ij+a(P_i+P_j)+bI

is affine in epsilon. Positive rational LDL pivots at both l and h therefore prove positivity at every point of I. Here v_ij is the sum of the two straight physical exchanges and P_i projects rung i onto its triplet space.

The independently audited weighted-star inequality gives the reference value

    f(A)=|A|-(3/10)[active edge weight + (1/2) sum_i maximal active incident weight]

for every occupied rung set A. Summing the local comparison and retaining the exact periodic multigraph multiplicities gives

    H(epsilon)-E00 >= D_a-B,
    D_a(A)=f(A)-4a|A|,    B=2Nb,    E00=-3N/4.

The bins enumerate all occupied subsets. Each block has rank 3^|A| and their ranks sum to 4^N. The vacuum has rank one and D_a=0. Every nonvacuum bin is strictly positive before subtracting B. Ordered min-max consequently supplies the uniform second-eigenvalue lower bound

    alpha = E00 + min_{A nonempty} D_a(A) - B.

This argument uses the full Hilbert space. The perturbation need not preserve occupied-rung sectors.

Every saved successful record verifies alpha>rho_max. The actual ground state is therefore unique. Temple's inequality and the endpoint bounds give, at every epsilon in I,

    rho(epsilon)-delta <= E0(epsilon) <= rho(epsilon),
    delta = R_max/(alpha-rho_max).

The energy width delta is independent of epsilon, but its center remains the exact affine rho(epsilon).

## Uniform heat traces and correlated energy cancellation

For seed volume i write rho_i, delta_i and the full reference bins as above. The shifted partition function obeys

    exp(beta rho_i(epsilon)) Z_i(beta,epsilon)
      <= exp(beta delta_i)
       + sum_{q>0} m(q,f) exp[-beta(E00_i+f-4a_i q-B_i-rho_i(epsilon))]
      <= Q_i(beta).

The final Q_i is obtained by replacing only the last rho_i(epsilon) by its endpoint maximum. Its ground contribution remains exp(beta delta_i). All 4^N-1 excited reference levels are included in the sum.

Order the seed geometries as i=0,1,2 for 2x2, 4x2 and 4x4. Each of the four combinations

    d_A(epsilon) = rho_1(epsilon)-2rho_0(epsilon),
    d_B(epsilon) = rho_2(epsilon)-2rho_1(epsilon),
    d_J1(epsilon) = 2rho_2(epsilon)-8rho_0(epsilon),
    d_J2(epsilon) = 4rho_2(epsilon)-8rho_1(epsilon)

is affine. Its maximum over I is computed directly from its two endpoints, after the extensive E00 terms have canceled exactly. Let these maxima be M_A,M_B,M_J1,M_J2. Uniform lower inputs are

    A >= exp(-beta M_A)/Q_0^2,
    B >= exp(-beta M_B)/Q_1^2,
    C >= 1/Q_2^2,
    J1 >= exp(-beta M_J1)/Q_0^8,
    J2 >= exp(-beta M_J2)/Q_1^8.

They follow from the same exact heat-trace identities as the audited point construction. In particular J1 is the exactly canceled combination A^4 B^2 C, and J2 is B^4 C^2 before the first update. Computing them directly avoids the loss from separately bounding correlated partition functions. The maximum of an affine energy combination is not replaced by a combination of independent energy maxima.

The first three updates use G(x)=1-(1-x)^2/(2x^2), with directed downward rational rounding,

    A1=G(J1),
    B1=G(J2 A1),
    C1=G(C^4 A1^2 B1).

The subsequent audited three-purity recurrence is unchanged. The stored 128-bit inputs are independently bounded by a distinct 192-bit Taylor implementation, and the final logarithmic gap is checked through an outward exponential inequality. Floating scans only choose the temperature. They do not decide validity.

## Every integer square side

The transfer construction and its real structure apply throughout every interval because the two layer-coupling eigenvalues are epsilon and 2J+epsilon, both nonnegative. The finite-window lemma in ../root_review/FINITE_WINDOW_INTERPOLATION.md is applied to the initial n=2 canonical state, the n=4 correlated state, and each following dyadic state before asymptotic acceptance.

Each exact finite-window record covers all integer sides n<=L<=2n, including odd L. Consecutive windows overlap and reach the asymptotic entry side. Every finite-window gap exceeds the saved asymptotic gap for the reported successful intervals. Thus the minimum is the displayed asymptotic value, and no short-size window is omitted.

## Dimensions and costs

The full Hilbert dimensions are 256, 65,536 and 4,294,967,296. The linear trial dimensions are 23, 93 and 377. Exactly one vector is retained for each geometry and each chosen vector epsilon. These are sparse rational Ritz vectors, not MPS states, so an MPS bond dimension is not assigned.

The full polynomial-action union contains 58, 1,301 and 21,345 rung-basis configurations. Full-spectrum completeness comes from the occupancy reference, not from this action support. No full many-body diagonalization and no new eigensolve was used. The initial four-interval construction took 13.8 seconds with peak process RSS 102,272 KiB on one CPU thread. Separate refinement cost is recorded in frontier_cost.json.

## Files, reproduction and open boundary

- extend_interval.py constructs polynomial, interval, heat and size certificates.
- extension_polynomials.json and extension_certificates.json contain the immutable first four intervals, including the unsplit final interval.
- frontier_polynomials.json and frontier_certificates.json contain the refined final intervals, the extension through 0.00855, and unsuccessful tested proposals.
- coverage_summary.json combines the selected intervals and checks endpoint adjacency exactly.
- extension_cost.json and frontier_cost.json record measured process costs.
- The vector and source-record paths and SHA-256 hashes in each polynomial record refer to immutable inputs in ../nonperturbative_audit/epsilon_scan.

Reproduce the first run from the repository root with

    PYTHONDONTWRITEBYTECODE=1 python research_20261010/epsilon_interval_extension/extend_interval.py

The second run's full command is saved in REPRODUCE.sh. Neither command changes baseline data or remote state.

The tested closed interval [0.00855,0.0086] did not yield a successful proposal on beta=12,12.5,...,120 with the specified fixed q<=2 vector and comparison optimizer. Additional tested intervals through 0.0088 also failed. This is an explicit gap beyond the reported coverage, not evidence of a phase transition, a maximal certifiable epsilon, or failure of all possible certificates.
