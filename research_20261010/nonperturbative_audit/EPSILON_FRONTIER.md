# Certified perturbation intervals and sampled points

Updated: 2026-10-10 13:27 EDT / 17:27 UTC.

The model throughout is the periodic square spin-1/2 bilayer with rung exchange 1, straight exchanges J+epsilon, crossed exchanges J, and J=3/10. Directions of length 2 keep both periodic adjacency terms. This report supplements, and does not modify, the independently audited fixed epsilon=1/200 result in `BASELINE_PROOF.md`.

## 1. A uniform interval certificate from one product trial

A new exact-arithmetic construction certifies

**0 <= epsilon <= 19/4000 = 0.00475: unique finite-volume ground state and Delta_L >= 0.008090283176 for every integer L >= 2.**

Its exact uniform lower bound is

2752980708324742958664216503824603161 / 340282366920938463463374607431768211456.

The actual trial space has dimension one: the product of rung singlets. For positive epsilon this is not an exact eigenvector. Its nonzero full residual is bounded explicitly. The maximum seed still has 32 physical spins and full Hilbert dimension 4,294,967,296, but only 97 configurations are reached by applying H to this product vector. No eigensolver, MPS or truncated excitation diagonalization is needed for this interval certificate.

Other independently checked uniform results from the same construction are:

| Uniform interval | Gap for every integer L >= 2 | Initial beta | Bootstrap entry side |
| --- | --- | --- | --- |
| 0 <= epsilon <= 0.004 | 0.024046763298 | 28 | 16 |
| 0 <= epsilon <= 0.0045 | 0.014475263367 | 27.5 | 32 |
| 0 <= epsilon <= 0.00475 | 0.008090283176 | 28.5 | 32 |

Every displayed gap is truncated downward. The machine-readable fractions are in `vacuum_interval_certificates.json`. The uniform claim follows from the interval argument below, not from interpolation between sampled epsilon values.

### Uniform local comparison

Fix epsilon_max. Construct rational a>=0 and b>0 and check both 16-dimensional physical-spin matrices

a(P_i+P_j)+bI,

epsilon_max v_ij + a(P_i+P_j)+bI,

by exact positive rational LDL pivots, where v_ij is the sum of two straight exchanges. The matrix at every epsilon in [0,epsilon_max] is their convex combination and is therefore positive. The same occupancy reference D_a-B from the fixed-parameter audit is consequently a valid lower operator for the whole interval.

The reference has one vacuum eigenvalue zero before subtracting B. Its next value gives a uniform positive second-level shift d. All bin counts still sum to the full dimension. The perturbation need not conserve occupations for min-max to apply.

### Exact full residual of the singlet product

Use the unit-normalized singlet product Omega. The shifted H_FF annihilates it and every straight bond has zero expectation, hence its Rayleigh quotient is exactly E00=-3N/4 for every epsilon. A two-rung calculation gives

||v_ij Omega||^2 = 3/4.

The independent physical-spin kernel verifies this identity exactly. Each nonzero vector v_ij Omega has triplets on exactly the endpoint pair i,j. Distinct unordered edges therefore give orthogonal vectors. Parallel edges have already been combined into their weight w_ij. Thus the complete residual squared is exactly

r^2(epsilon) = (3/4) epsilon^2 sum_{i<j} w_ij^2.

The sums of squared edge weights are 16, 24 and 32 for the 2x2, 4x2 and 4x4 seeds. Their residual squared values are respectively 12, 18 and 24 times epsilon^2. This accounts for all states reached by H Omega, rather than a projected residual.

Temple's inequality with the uniform second-level shift d gives, for every epsilon in the interval,

E00 - r^2(epsilon_max)/d <= E_ground(epsilon) <= E00.

These uniform endpoints and the uniform complete occupancy-bin reference bound every partition function in the interval. The thermal inequalities and correlated recursion are then exact copies of the audited mathematical construction, with no epsilon-dependent unverified input. The separate 192-bit rational exponential verifier checks the resulting 128-bit inputs and recursion.

### Stronger bridge using triangle-free square graphs

The short-size bridge in the fixed epsilon=.005 theorem already suffices for that theorem. Larger bootstrap entry sizes benefit from the following additional finite-volume comparison.

For every square L>=4, the nearest-neighbour graph is simple, degree 4 and triangle-free. In an occupied set of size q, let E be the number of active edges. Degree counting gives E<=2q. Triangle-freeness gives E<=floor(q^2/4): for each edge ij, the active degrees obey d_i+d_j<=q. Sum over edges and apply Cauchy-Schwarz to obtain 4E^2/q<=sum_i d_i^2<=qE. This also handles E=0 directly.

The weighted-star bound from the baseline proof, with all active weights equal to 1, therefore gives

f(q) >= q - (3/10)[min(2q,floor(q^2/4))+q/2], q>=2,

and f(1)=1 exactly. The eight reference values for q=1,...,8 are

1, 7/5, 39/20, 11/5, 49/20, 12/5, 47/20, 2.

For q>=8 the simpler bound f(q)>=q/4 applies. If 0<=a<1/16, then f(q)-4aq is bounded for all q>=8 by its q=8 lower value. Consequently the minimum nonvacuum reference value on every such square is at least

c(a) = min_{1<=q<=8}[f(q)-4aq].

Using a separately certified local comparison gives

lambda_second(H_epsilon shifted) >= c(a)-2L^2 b.

Again the vacuum trial expectation is zero, so this is also a lower bound on the actual gap. For all 4<=L<n, use L=n-1 on the right. L=2 and L=3 are covered independently by 2/5-12epsilon_max and 1-27epsilon_max. Local PSD at both epsilon endpoints makes this entire bridge uniform on the interval.

For epsilon_max=19/4000 and n=32 the certified minimum bridge is 343/1000, much larger than the thermal gap. This closes all missing sizes. The exact chosen a,b, all eight levels and all bridge arithmetic are saved in the certificate.

`certify_vacuum_interval.py` constructs the uniform certificate. `trianglefree_bridge.py` contains the separate exact bridge check. `INTERVAL_INDEPENDENT_REVIEW.md`, when present, records a second review of the new argument and arithmetic.

## 2. Individually certified nonzero epsilon values

The existing q<=2, total-Sz=0 trial spaces have dimensions 23, 93 and 377 for the three seed geometries. Exactly one Ritz vector per geometry is retained. For every new point below, the full exact sparse residual, local PSD, occupancy bins, Temple enclosure, thermal inputs and successful recurrence were independently audited.

| epsilon | Certified gap | Integer square scope | Initial beta | Entry side |
| --- | --- | --- | --- | --- |
| 0.005 | 0.038983227177 | Every L>=2 | 32 | 8 |
| 0.006 | 0.028171615330 | Every L>=2 | 28 | 16 |
| 0.0075 | 0.012626894873 | Every L>=2 | 31.5 | 16 |
| 0.008 | 0.008498663753 | Every L>=32. Smaller-size bridge open | 32 | 32 |
| 0.0085 | 0.001984903734 | Every L>=128. Smaller-size bridge open | 32.5 | 128 |

At epsilon=.0075, a slightly stronger bootstrap bound 0.013466260266 holds for L>=32, but its all-smaller-size bridge has not been closed. The all-L value displayed above uses the n=16 certificate instead.

For the n=16 all-size bridges, the simpler sector argument already suffices: H_FF>=Q/4 plus exact q=1,2,3 estimates implies the nonvacuum reference lower bound 1-16a for 0<=a<1/16. Thus Delta>=1-16a-2L^2b for 3<=L<16, combined with the period-2 bound. The exact bridge minima are 0.328 at epsilon=.006 and 0.167536407950 at epsilon=.0075. They exceed the thermal bounds.

These point certificates do not by themselves establish the intervening continuum of epsilon values. The interval theorem in Section 1 is separate and explicit.

## 3. Scope of negative scan observations

The floating proposal grid scanned initial beta=12,12.5,...,120 with the recorded q<=2 trial vectors, occupancy-star reference and local parameter optimizer. No successful proposal was found at epsilon=.009,.01,.0125,.015 or .02. Selected temperatures were then evaluated exactly and also failed the scalar recursion.

This is not a no-go theorem over all beta, all local comparison parameters, larger trial spaces, improved spectral tails or different seed geometries. In particular it is not a physical phase transition, a maximal epsilon or proof of a closed gap.

For the one-product-trial interval construction, epsilon_max=.005 has no success on the same beta grid. This is fully consistent with the successful fixed epsilon=.005 optimized Ritz certificate: the product trial has a larger nonzero residual. No optimality claim is made about epsilon_max=.00475.

## 4. Artifacts and reproducibility

- `epsilon_scan_summary.json`: sampled points, exact selected seeds and simple finite bridges
- `epsilon_scan/`: every generated ground vector and record, with selected exact thermal seeds
- `ff_eps*_selected_seeds_audit.json`: independent exact audits of sampled inputs
- `trianglefree_bridge_scan.json`: additional bridge checks, including unsuccessful bridge attempts
- `vacuum_interval_certificates.json`: uniform interval proof inputs and exact outputs
- `epsilon_scan.log`, `epsilon_refinement.log`, `trianglefree_bridge.log`, `vacuum_interval.log`: execution logs

From the repository root:

    PYTHONDONTWRITEBYTECODE=1 python research_20261010/nonperturbative_audit/scan_epsilon.py
    PYTHONDONTWRITEBYTECODE=1 python research_20261010/nonperturbative_audit/scan_epsilon.py 1/125 17/2000 9/1000
    PYTHONDONTWRITEBYTECODE=1 python research_20261010/nonperturbative_audit/trianglefree_bridge.py
    PYTHONDONTWRITEBYTECODE=1 python research_20261010/nonperturbative_audit/certify_vacuum_interval.py

The first two commands produce proposals and then audit them. The last command uses an analytic product-state residual and no Ritz solve. Exact matrix and spectral assertions, not floating proposal values, determine certification. All saved files are new files in this audit directory. The original checkpoint was not edited. BLAS is limited to one thread per process. No more than two CPU processes were run concurrently and observed memory remained far below 2 GiB.
