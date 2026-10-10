# Low-energy-only deterministic purity seeds

Checkpoint: 2026-10-10. All source code and generated results here are new; the uploaded original is unchanged.

## What is certified

The accepted input endpoints use integer arithmetic, Python `Fraction`, and rational exponential remainder bounds. Floating eigensolvers only propose a single trial vector. Their residuals are never treated as proof of spectral completeness. No full finite-system diagonalization enters these certificates.

Successful examples already saved:

- Interacting spin-1 alternating chain, strong bonds 1 and weak bonds 1/20. Two-/four-cell seed, beta=10: S>=0.930080341751, T>=0.946623580846. Original exact scalar replay accepts in two rounds and yields 0.116303868802 for all even cell counts >=8. Original all-integer interpolation plus the separately checked short-size bound 1-M/10>=0.3 extends this to every cell count M>=2. Independent audit of matrices, exact residuals, and all replay steps is in the sibling `audit/independent` directory.
- Width-two open-transverse spin-1/2 columnar strip, horizontal and transverse weak couplings both 1/50. At beta=12: S>=0.995737067529, T>=0.994822938683, accepted immediately. Conditional gap 0.304506648715, all axial M>=2 under the strip transfer proof. This is a fixed-width theorem, not width-uniform two-dimensional control.
- Same strip at couplings 1/20: beta=20 gives S>=0.961810621191, T>=0.985798983863 and gap 0.093972140261 after scalar contraction (see JSON for exact length scope).
- Genuine square spin-1/2 bilayer, unit AF rungs and in-layer AF x/y couplings both 1/100. At beta=20, A>=0.993912845069751, B>=0.987823277605056, C>=0.996973815517648. The sibling three-purity exact replay accepts after one round and returns square gap 0.072950533962 for every integer square side L>=4, conditional on both transfer hypotheses proved separately. Only one Ritz vector is used in each 8-,16-,32-spin patch. Trial dimensions are 23,93,377, versus full Hilbert dimensions 256,65536,4294967296.
- Bilayer couplings 1/50 succeed with the improved local relative-form bound. At beta=12, A>=0.984164773935285, B>=0.966241783973469, C>=0.976538105117227; three-purity replay accepts in three rounds and yields 0.030629385475 for integer square side L>=16. This is not yet a claim about every small square; bridge those separately.

No claim is made here that the uniform spin-1 Heisenberg chain or a uniform undimerized two-dimensional antiferromagnet has been certified. Coupled-dimer models are a controlled testbed for a rigorous replacement of full ED.

## Proof, independent of floating diagnostics

Let H0 be N disjoint spin-s dimers with unique product-singlet ground energy E00=-Ns(s+1). Its excitation generating function is z_s(t)^N, where z_s(t)=sum_(J=0)^(2s)(2J+1)exp[-t J(J+1)/2]. Let H=H0+V.

1. A deterministic full-space inequality supplies H >= E00 I + alpha(H0-E00 I)-B I. The simplest choice is alpha=1 and B=-sum_e lambda_min(v_e), a sum of exact local bond minima. By the min-max principle, every ordered eigenvalue satisfies E_j(H)>=E00+alpha*epsilon_j(H0)-B. In particular, E_1(H)>=a=E00+alpha-B. This is the no-missed-state/complement certificate, across ALL symmetry sectors.
2. A single normalized trial vector has exact Rayleigh quotient rho and squared residual r2. If rho<a, the variational principle proves that exactly one eigenvalue lies below a. Temple's inequality gives rho-r2/(a-rho)<=E0<=rho. The trial vector need not be a highly accurate Ritz vector and can live in any sparse support.
3. With e+=rho, e-=rho-r2/(a-rho), define Q=exp(beta e+) Tr exp(-beta H). Then 1<=Q<=exp[beta(e+-e-)]+exp[-beta(E00-B-e+)]*[z_s(alpha beta)^N-1]. The final bracket counts ALL excited H0 eigenvalues with exact multiplicity. Ordered spectral comparison transfers it to ALL omitted eigenvalues of H. No states are discarded by a probabilistic estimate.
4. For two sizes, S>=exp[-beta(e+_(2n)-2e+_n)]/(Q_n^+)^2 and T>=1/(Q_(2n)^+)^2. For a bilayer, apply this successively to 2x2,4x2,4x4 and feed the three exact lower endpoints to the separately audited recursion.

A short proof of the Temple step: for every eigenvalue lambda, (lambda-E0)(lambda-a)>=0 because E0 is the only eigenvalue below a. Its expectation in the trial vector is nonnegative, so r2+(rho-E0)(rho-a)>=0 and E0>=rho-r2/(a-rho).

### Improved local form bound

For adjacent dimers, certify the fixed-dimensional matrix inequality

 g v_ij + a_loc(h_i+h_j)+b I > 0,

where h_i is the isolated dimer excitation operator. All entries are rational in an orthogonal unnormalized dimer basis. Multiply by its positive diagonal metric and clear denominators; exact fraction-free symmetric inertia verifies positive definiteness. On a periodic bilayer of N rungs there are 2N lattice edges with multiplicity, each rung degree four, hence alpha=1-4a_loc and B=2Nb.

Example: spin-1/2, g=1/50, N=16, a_loc=17/400, b=2163649829/500000000000. Exact local inertia is (negative,zero,positive)=(0,0,16), alpha=83/100, B=2163649829/15625000000. The second-level lower shift improves from the naive 0.04 to 0.691526410944. Local floating diagonalization merely proposes b, then exact inertia accepts or rejects it.

### Sparse-support verification

`dimer_subspace.py` constructs an orthogonal rational eigenbasis of each two-spin dimer, with positive diagonal Gram matrix G. The trial space includes at most two excited dimers and total Sz=0. A single Ritz vector is rounded to integers v in this basis. The code constructs the entire rectangular map H from trial support into EVERY reached configuration, including four-excitation configurations outside the trial space. It computes

 rho=(v^T G H v)/(v^T G v),
 r2=((Hv)^T G (Hv))/(v^T G v)-rho^2

exactly. Ignoring the outside-support terms would invalidate the certificate; they are explicitly included and independently checked on small patches.

For the 32-spin g=.01 bilayer, the trial has 377 basis states; Hv occupies 21345 possible basis states. Runtime was 0.74 s and peak RSS about 85 MiB in the initial benchmark; complete-space dimension is 2^32. This is a computational reduction for these controlled models, not a claim of polynomial complexity for arbitrary Hamiltonians or precision.

## Files and commands

- `ground_tail.py`: explicit rational Sz-sector matrix, one full-sector Ritz vector, exact verification and original scalar replay.
- `dimer_subspace.py`: sparse dimer-excitation trial and exact leaked residual, allowing enormous formal Hilbert spaces.
- `local_relative_bound.py`: local exact-inertia relative form bound, full-spectrum bin transfer, improved Temple interval.
- `bilayer_seed.py`: exact three-purity inputs and replay; depends on sibling `two_d_theory/three_purity_certificate.py`.
- `*_trial.npz` / `*_ritz.npz`: exact integer trial vectors and metadata.
- `*_ground.json`: rational Rayleigh, residual, energy bounds and graph.
- `certificate_*.json`, `bilayer_seed_*.json`: full replayable seed records, including failed proposals.

Run with single-thread BLAS, for example:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python ground_tail.py --spin 1 --g 1/20
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python bilayer_seed.py --g 1/50 --relative --betas 12,16,20

Memory limit is 3 GiB and worker CPU budget two. Current calculations are far below it. No long job should start without a checkpoint and a support/memory estimate.

## Method comparison and limits

- Exact global LDL/inertia: robust spectral counts with no floating rounding issue; original spin-2 L4 test demonstrates it. Exact dense fraction-free elimination becomes unattractive for the spin-1 L8 Sz0 block (1107) because fill and integer bit growth are not controlled. Here exact LDL is instead used on fixed local 16x16 or81x81 matrices, where it is cheap.
- Block Gershgorin / complement lower bounds: a local relative-form inequality is a structured substitute and controls all omitted states by min-max. Plain entrywise Gershgorin in the physical Sz basis is generally much looser for a singlet ground.
- Symmetry-resolved bins: total-Sz symmetry reduces the trial solve only. Completeness is NOT inferred from that sector. The dimer generating polynomial supplies exact whole-space counts, so all magnetization and spin multiplets are included automatically.
- Deflation plus polynomial tail: the certified ground term is deflated explicitly. The remaining exact generating polynomial in exp(-alpha beta) is a deterministic tail bound. This is stronger here than multiplying one cutoff Boltzmann factor by the entire Hilbert dimension.
- Approximate LDL with rigorous roundoff: not yet used. It would require an explicit outward norm bound on the factorization residual and a protected inertia interval, not merely a computed floating LDL or observed pivot signs. Suitable primary references are listed below.
- Uniform strongly coupled models: the present dimer lower bound becomes too weak; no valid missing-state certificate is obtained just by carrying a Ritz vector to stronger coupling. Failed scalar seeds and failed complement bounds remain failures.

## Primary technical sources

The proof above is self-contained; these give broader verified-eigenvalue context.

- S. T. Kuroda, Estimates of Kato-Temple Type for n-dimensional Spectral Measures, Publ. RIMS43 (2007),505–520: https://www.kurims.kyoto-u.ac.jp/~prims/pdf/43-2/43-2-24.pdf
- L. Grubisic, On Temple-Kato like inequalities and applications: https://arxiv.org/abs/math/0511408
- N. Yamamoto, A simple method for error bounds of eigenvalues of symmetric matrices, Linear Algebra Appl.324 (2001),227–234: https://doi.org/10.1016/S0024-3795(00)00274-3
- S. M. Rump, Verified Error Bounds for All Eigenvalues and Eigenvectors of a Matrix, SIAM J. Matrix Anal. Appl.43 (2022),1736–1754: https://doi.org/10.1137/21M1451440

These outputs are executable exact-arithmetic certificates, not formal proof-assistant verification. The analytical transfer and interpolation hypotheses are recorded separately by the audit and two-dimensional theory workers.
