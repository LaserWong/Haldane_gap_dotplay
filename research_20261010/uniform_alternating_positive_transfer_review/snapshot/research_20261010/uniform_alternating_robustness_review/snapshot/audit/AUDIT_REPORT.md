# Independent audit of Haldane_extensions

Audit date: 2026-10-10 UTC. Original files were read only. All computation was written under `audit/`, with BLAS/OpenMP thread counts set to one. This audit concerns the uploaded extension package, not an independently supplied original spin-one proof.

## Executive verdict

1. The advertised alternating-chain certificate survives independent scrutiny: under the precise homogeneous-cell hypotheses below, the proof establishes a unique periodic ground state and a gap at least **0.055688426272** for every integer number M >= 2 of two-spin cells. It does not require numerical diagonalization or a long-chain numerical seed.
2. The three included exact demonstrations reproduce from scratch. An independent angular-momentum calculation also validates the four-site heat moments, spectral counts, and heat-trace enclosures.
3. The uniform spin-2 and spin-3 Heisenberg chains are **not** certified by the extension package. Its saved spectra are floating diagnostics. The original-method archive was separately recovered during this audit; see the provenance update below. The original manuscript PDF is still absent.
4. No finite-width cylinder calculation by itself proves a width-uniform two-dimensional gap. A 2D proposal needs a separate closure/interpolation theorem and certified seeds with explicit area, aspect-ratio, and boundary conventions.
5. One literature qualification is needed: the cited **block** Gauss/Radau paper proves two-sided matrix-order results for resolvents/Stieltjes functions. It does not supply a general certified block exponential bound merely from its exponential numerical experiments. Scalar Gauss/Radau heat-function quadrature remains a valid avenue with verified endpoints and arithmetic.

## Reproduction ledger

The 59 file entries in `SHA256SUMS.txt` all match. This proves package integrity relative to its included manifest, not authenticity of earlier material or correctness of claims.

Fresh copies of the seven scripts were placed in `reproduction/code/`. Its results directory began empty, so `exact_heat_trace.py` rebuilt all moments without loading the uploaded cache. Commands:

```
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python code/analytic_certificates.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python code/exact_heat_trace.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python code/inertia_trace.py
```

Results:

- `analytic_dimer_certificates.json`: identical parsed JSON to upload.
- `integer_heat_trace_moments.json`: identical parsed JSON; all 201 exact moments match.
- `inertia_tail_certificate.json`: identical parsed JSON.
- `exact_heat_trace_certificate.json`: identical exact contents after removing the original's downstream floating-ED comparison annotations. No spectrum file was supplied to this fresh run.
- Heat trace beta=1: displayed 1175006755.8835309, certified relative width approximately 7.992473464364571e-63.
- Heat trace beta=2: displayed 3.339466244233213e17, certified relative width approximately 8.21814434866937e-24.
- Counts below -20.5, -19.5, -18.5, -16.5, -15.5: exactly 0, 1, 4, 9, 9.
- Nine-state beta=8 omitted-tail relative upper bound: approximately 1.4273895556065162e-13.

Independent verifier `independent/verify_baseline.py` imports **no original or copied project module** and calls no eigensolver. It uses H4 = A·B with A=S1+S3, B=S2+S4. Pair angular momenta a,b range from 0 to 4; total j ranges from |a-b| to a+b; energy is [j(j+1)-a(a+1)-b(b+1)]/2 with multiplicity 2j+1. This enumerates dimension 625 exactly. Every moment of B_int=32I-2H through degree 200 matches the archive. Independent rational exponential enclosures of the exact heat traces are contained inside both packaged certified intervals.

The independent scalar check uses a fixed 300-term positive Taylor series and rational geometric remainder. It reproduces the four rounded bootstrap rounds and verifies the final logarithmic gap by the alternative test exp(96*0.055688426272) < 1/(5u), with u=19067031/20000000000. Details are in `independent/baseline_verification.json`.

## Exact scope of the transfer-kernel argument

For the dimer theorem the model must be

H_M = sum_i S_(i,R)·S_(i+1,L) + sum_i v_i,

where all cells have the same finite spin s and every v_i is a translate of one **Hermitian**, fixed, two-spin operator v. The single-transfer-power representation requires this homogeneity. Merely bounding unrelated disordered v_i does not justify writing Tr X^M.

Necessary cell assumptions are:

- time reversal Theta_s tensor Theta_s fixes v;
- the left/right exchange F fixes v;
- width(v)=lambda_max(v)-lambda_min(v) <= 3/100;
- periodic boundary conditions and M >= 2 in the history construction;
- fixed s while taking chain length to infinity. The gap bound is numerically independent of s, but the Hilbert space and locality constants are not a single unbounded-spin system.

Because cell time reversal squares to +1 for both integer and half-odd-integer s, choose a cell basis in which it is complex conjugation. Time-reversal-odd spin components are then i times real antisymmetric matrices. v is real symmetric and F real orthogonal. The bond exponential expansion has nonnegative history measure and bounded local real kernels. Conjugation by F swaps the two boundary histories without reversing their time order. Thus k(xi,zeta)=k(zeta,xi). This does not require the kernel to be entrywise positive, or X to be positive semidefinite.

Using B_alpha=A_alpha/s gives operator norm at most one. The one-bond history measure has finite mass exp(3 beta s^2), while |k| <= (2s+1)^2 exp(beta ||v||). The kernel therefore defines a self-adjoint Hilbert–Schmidt operator. For each fixed finite M, absolute convergence permits regrouping Duhamel histories by bonds and cells, including M=2 with its two distinct strong bonds. Contracting the resulting bounded cyclic kernel gives Tr X_beta^M = Z_M(beta). For M>=2 the powers are trace class. Equal-time coincidences between independent nonempty histories are measure zero and do not obstruct ordering.

The same X_beta works for all integer M. That last statement is indispensable for the odd-length argument. Showing only even moments would not rule out a negative dominant transfer eigenvalue.

## Purity recursion: checked algebra and order

For even n, X_beta^n/Z_n is positive and has trace one, whether or not X_beta is positive. Its purity is S=Z_2n/Z_n^2. The Gibbs purity is T=Z_2n(2beta)/Z_2n(beta)^2.

For any probability sequence, normalizing its square gives defect at most f(u)=u^2/[2(1-u)^2]. The bound follows from the nonnegative pairwise cross terms and is valid whenever 0<=u<1. This is an upper bound, not an exact recurrence for a many-level spectrum.

The spatial update uses S(n,2beta)>=S(n,beta)^2 T(2n,beta), then squares the spatial density. The thermal update first uses T(4n,beta)>=S(2n,2beta) T(2n,beta)^2, then squares the Gibbs state. Therefore the second update must use the newly obtained p'. The code does so, with every defect rounded upward to 12 decimal places.

Once p,q<=u<=0.01, the checked monotone coefficient bounds imply both updated defects <=5u^2. The code's finite-precision replay is used only to reach this small region. The subsequent arbitrary-length theorem uses the exact analytic inequality, not repeated rounded computation that would hit a 1e-12 floor.

## Dimer seed: checked ingredients

Subtract tr(v)/(2s+1)^2 from v. In the unperturbed strong-dimer Gibbs state each cell's two spins come from different independent dimers for M>=2, so its reduced density matrix is maximally mixed and the perturbation has zero expectation. Its total spectral width is at most Mw.

The Gibbs variational lower bound and Golden–Thompson upper bound reduce the partition-function ratio to a classical spectral measure of V. Hoeffding's lemma then gives 0 <= log Z_M-log Z_M^(0) <= beta^2 M^2 w^2/8. No commutation between H0 and V is assumed. The quadratic-in-M estimate is used only for the initial small seed, not at arbitrary length.

For isolated dimers, z_s(beta)=sum_(J=0)^(2s) (2J+1)exp[-beta J(J+1)/2]. The spin-uniform upper bound at beta=6 uses a J>=2 geometric tail. At n=2 and w=0.03 the lower purities are S>=0.968119256916 and T>=0.827889278688. Four sequential rounds produce n*=32 cells, beta*=96, u=0.00095335155. The gap follows for M>=32; Weyl's inequality covers 2<=M<=31 by Delta_M>=1-Mw>=0.07.

The general v, M=1 observation is separately justified by a one-dimer width perturbation bound; it is not an extra use of the cyclic transfer construction.

## All-integer interpolation: checked, including signed spectrum

Set Y=X_(2beta). Its normalized n-th spectral powers have purity at least (1-u)^3>1/2, so their largest weight is unique and greater than 1/2. Since n is even, it identifies a unique eigenvalue of largest absolute value. That eigenvalue must be positive: otherwise its contribution would make sufficiently large odd traces negative, contradicting Z_M(2beta)>0 for all integer M.

The largest weight exceeds 1-2u, yielding r=sum_(a>0)|mu_a/mu_0|^n <= 2u/(1-2u). For every integer L>=n, the tail is at most r^(L/n). This is the l^p inequality applied at exponent L/n>=1; using a 2n-th moment for an L<2n tail would be invalid, but the report does not make that error.

For n<=L<=2n, the numerator lower bound uses the positive dominant eigenvalue and subtracts the absolute tail. The denominator uses Holder interpolation of the absolute spectrum of X_beta between its n-th and 2n-th moments. These endpoints are even, so those moments equal the physical partition functions. Signed odd traces cause no problem because Z_L <= sum |lambda|^L.

Together these give T(L,beta)>=1-4u. A probability distribution with purity above 1/2 has a unique largest entry; for a Gibbs state this establishes a unique ground state. Moreover p_1/p_0<=4u/(1-4u)<=5u, so Delta_L>=log[1/(5u)]/beta. Choosing a dyadic n_j<=L<=2n_j and using u_j<=(5u_0)^(2^j)/5 gives the common bound for every integer L>=n_0. No thermodynamic/zero-temperature limit interchange occurs.

## Provenance and interpretation gaps

### Update after recovering the original archive

At 16:00 UTC on 2026-10-10 the parent separately recovered `upstream/extracted` from HaldaneConjecture.zip. Its archive SHA256 is f55ab851502759d863673f627bce28de1d040750f18f747a7814e866153425c8; the extensions archive SHA256 is 01083339c21f8da1f642c72fa49b642b1ba55d3864bdd29485a1fc2609a42c97. The original archive contains 12670 entries, including directories and historical snapshots. Its built-in manifest independently passes all **8464** listed file hashes and sizes, recorded in `upstream_integrity.json`. The extensions scalar script is byte-identical to the recovered original `tools/bootstrap_scalar.py`. Original policy, technical guide, current-results ledger, and verification scope have now been read. The original PDF remains absent.

The following initial-package limitations explain what was missing from the extensions ZIP alone; the recovered original now supplies the named documents and many physical input files. It still does not convert cached postprocessing into a from-scratch physical recomputation. The recovered verification ledger explicitly states that only 9 physical reference heat kernels were independently rebuilt, while 27 printed totals were arithmetically checked; the original manuscript audit is partial.

### What the extensions ZIP alone supplied

Absent from this ZIP are the report's cited original `PROJECT_OVERVIEW.md`, `INSTRUCTIONS.md`, `docs/TECHNICAL_GUIDE.md`, `docs/CURRENT_RESULTS.md`, original heat-kernel audit code, complete physical-input/block certificates, spin-2 `verified_real` manifests and referenced blocks, ninth/tenth-order certification inputs, and the original manuscript titled “The periodic spin-one Haldane gap.” The saved three manifest SHA256 strings cannot authenticate missing files. The copied scalar script's “unchanged original” status also cannot be checked without that original copy.

Before recovery, consequently the earlier BLBQ eta=-0.05 long-chain bound, spin-2 eighth-order certification claim, tenth-site high-magnetization tails, global exclusion of a former beta=9/4 seed, and the n=4 all-temperature exclusion are report-level assertions here. They are not newly checked physical certificates in this audit.

The `archived_spin2_L8.npz` file contains floating energies, not interval eigenvalue enclosures or a completeness proof. Filename words such as “verified” in its provenance do not change that. Similarly, a small Ritz residual does not certify that an omitted eigenvalue cannot be lower. A low-energy-only seed needs certified eigenvalue enclosures **and** spectral counts or a complement lower bound, plus certified finite-chain ground-energy differences.

The “minimal n=2” statement means the smallest even n accepted by this particular transfer-purity interface. It is not an optimality theorem among all gap proofs, minimum required numerical Hilbert dimension, or a uniform-Heisenberg minimum length. For this analytic dimer proof the number of numerically solved seed eigenvalues is zero. Distinguish physical chain length, number of cells, maximum transfer moment (physical length), and polynomial degree of a fixed-chain heat trace; K=200 here is not a 200-site transfer input.

## External theorem checks and recommendations

- Gosset–Mozgunov Theorem 3 applies to homogeneous, nearest-neighbor, frustration-free **projector** interactions. Its explicit bound is (5/6)[(n^2+n)/(n^2-4)](epsilon_n-6/[n(n+1)]) for periodic length m>2n. The AKLT local sum of orthogonal projectors meets projector normalization, but a floating seven-site crossing still needs a certified positive-gap lower bound and exact kernel/complement control. Smaller periodic lengths require their own treatment if a literal all-length number is claimed. [Primary theorem](https://arxiv.org/html/1512.00088)
- The 2026 SDP hierarchy publication is real and includes finite-size criteria as feasible certificates. Numerical optimizer output needs validated feasibility/rounding before being called a proof. [Primary paper](https://arxiv.org/abs/2411.03680)
- The cited block-quadrature theorem primarily concerns positive-real resolvents and their Stieltjes integrals. Its matrix exponential examples should not be presented as the same proven matrix-order enclosure. Use scalar quadrature with a rigorous derivative-sign theorem or independently validate the block exponential remainder. [Primary paper, sections 1 and 5–7](https://arxiv.org/html/2407.21505v3)
- The dimer SPT label additionally assumes the protecting SO(3) or D2 symmetry is retained along lambda v. Fixing the two-site cell makes the on-cell representation linear; half-odd-integer edge spins have nontrivial projective commutation. The uniform gapped path, rather than just a short-chain gap, supports continuation. [Symmetry protection](https://arxiv.org/abs/0909.4059), [spectral flow](https://arxiv.org/abs/1102.0842)

The most actionable new-proof risks are: missing physical-input completeness, signed-spectrum odd-length interpolation if transfer assumptions change, unverified long-width uniformity in 2D, energy-shift consistency between different lengths, and accidental use of floating residuals or unvalidated SDP output as lower bounds.
