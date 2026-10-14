# Independent two-dimensional numerics and certificates

This document records the numerical results available on October 10, 2026. The historical pause and pending calculations are described in `PAUSED_STATUS.md`. Current work follows the repository README and AGENTS.md. The uploaded source remains unchanged.

## Main findings

1. The spin-1 square model H = sum_i (S_i^z)^2 + g sum_<ij> S_i·S_j, with D=1 and nonzero g in both spatial directions, has a new exact-rational three-purity seed at g=1/100, beta=12. On the 2x2, 4x2 and 4x4 periodic patches the certified lower bounds are A>=0.9898383806359963, B>=0.9790341376100279, C>=0.9928327376166918. The three-purity replay returns a uniform square-gap lower bound 0.086452285325. The successful independent audit, including the all-integer L>=2 bridge, is recorded in `../audit/independent/largeD_g001_audit.json`. The transfer theorem is proved outside this numerical code.
2. The largest patch in this certificate contains 16 spin-1 sites, full dimension 43,046,721. It uses one Ritz vector on 241 product configurations and 8,321 configurations reached by the complete Hamiltonian action. Every accepted matrix operation, Rayleigh quotient, residual squared, spectral comparison and thermal bound uses exact integers/rationals. Floating eigsh only proposes the vector.
3. Independently expanding the low-energy calculation's bilayer trial vectors into full physical spin bases reproduces its rational Rayleigh quotients and complete residuals exactly for 8- and 16-spin examples at g=.01 and .02. Both spin-1/2 and spin-1 dimer kernels match independent rational Clebsch-Gordan constructions entry-for-entry.
4. Full, symmetry-blocked diagnostics on spin-1 large-D 2x2 to 4x2 patches pass the fixed-width two-purity recursion at g=.05 over beta 5.75--11, but fail at g=.1 on the sampled grid. These are floating-point finite-width diagnostics, not true-2D certificates.
5. Isotropic square Heisenberg controls have positive finite gaps and nevertheless fail the same small-seed purity test. The spin-1/2 periodic 4x4 gap is approximately 0.578598335765. This illustrates why a small-system gap is not a thermodynamic certificate. It is not a numerical proof of gaplessness.
6. An independent commuting spin-1 control has nonzero interactions in both directions, an analytically unique product ground state and exact gap 1. Its 4x4 trace is enumerated through 65,536 weighted binary occupancy patterns instead of 43 million spin states. It passes the exact three-purity replay.

## Geometry and basis conventions

- Physical spin digit a represents m=a-s. Site zero is the least significant digit.
- Square site index is x*ny+y. Columnar site index is 2*(x*width+y)+a, a=L/R.
- Periodic Hamiltonians use one +x and one +y term per lattice site. At length two this means two parallel lattice-bond terms. A deduplicated simple graph is exposed only as a separate diagnostic and must not be used in a periodic transfer family.
- The bilayer has one strong interlayer dimer per base-lattice vertex and weak same-layer edges in both base directions.
- The columnar strip has strong R(x,y)-L(x+1,y) dimers, weak intracell L-R bonds and weak vertical bonds on both legs. Open versus periodic transverse boundaries are explicit metadata.
- SU(2) checks apply to Heisenberg graphs. The single-ion large-D model has U(1) and spin-reversal symmetry, not full SU(2).

## Exact large-D comparison

Let n_i=(S_i^z)^2. The 9x9 two-spin inequality

    g Si·Sj + a(n_i+n_j) + b I >= 0

is verified by its magnetization blocks. With d=2a-g, the nontrivial 2x2 block has diagonal b and d+b and off-diagonal sqrt(2)g. The code verifies b(d+b)>=2g^2, a+b>=g and the remaining nonnegative diagonal conditions using exact fractions. An upward rational square-root enclosure chooses b.

On a periodic square multigraph every site has degree four and there are 2N edge terms. Consequently H >= c H0 - B I, c=1-4a>0, B=2Nb, H0=sum n_i. Ordered eigenvalue comparison gives lambda_1(H)>=c-B. A certified Rayleigh quotient rho<c-B identifies the unique full-Hilbert-space ground state, and Temple gives

    rho - residual_squared/(c-B-rho) <= E0 <= rho.

The residual includes all states reached outside the trial space. The omitted trace is bounded by the exact full reference degeneracy polynomial:

    tail <= exp[beta(B+E0_upper)] * [(1+2 exp(-beta*c))^N - 1].

Only a proposal search for a uses floats. Every selected a,b,c,B and every final exponential bound is rationally verified. Ground-interval width is retained in the shifted trace bound. No spectral-completeness claim is inferred from small Lanczos residuals alone.

## Main source and artifacts

- `models.py`: graph factories, resource-guarded fixed-Sz basis and sparse Hamiltonians, full small-sector spectra, low levels, independent tensor-product reference.
- `test_models.py`: graph counts, spin-pair spectra, full-vs-block matrix/spectrum agreement, SU(2) ladder commutators, dimer limits, sparse-vs-dense checks and large-D reference.
- `run_initial.py`: checkpointed spin-1/2 and spin-1 square, large-D and bilayer diagnostics.
- `crosscheck_certificates.py`: independent audit of the independently generated integer and dimer-basis certificates.
- `large_d_certificates.py`: exact sparse-support single-ion certificate and affine thermal comparison.
- `check_large_d.py`: independent full physical-Sz reconstruction of its exact quotient and residual for 2x2/4x2 patches.
- `large_d_pair_support.py`: extension using disconnected two-bond virtual-pair configurations for larger seed-size experiments. Status must be read from its own output.
- `commuting_control.py`: exact occupancy histograms and three-purity control.
- `results/largeD_g1d100_q2_certificate.json`: accepted interacting large-D certificate.
- `results/largeD_independent_checks.json`: direct physical-spin checks.
- `results/certificate_crosschecks.json`: independent checks of shared low-energy artifacts.
- `results/purity_scans.json`: all sampled fixed-width S,T curves, including unsuccessful points.
- `results/commuting_control_certificate.json`: exact commuting-control histogram and replay.
- Hashed numerical files carry the full graph, dimensions, method, boundaries, timing and `certified:false` marker. Hashes are model fingerprints, not evidence of mathematical certification.

## Resource and reproducibility policy

All calculations run with OPENBLAS_NUM_THREADS=1, OMP_NUM_THREADS=1 and MKL_NUM_THREADS=1. Tiny full-Hilbert Kronecker references are limited to dimension 1,000. Full dense symmetry blocks are limited to dimension 2,000. Sparse physical basis allocation is guarded before construction. No full 16-spin-1 or 32-spin-1/2 ED is attempted. Larger support experiments run with a 2.5 GiB address-space ceiling, below the assigned 3 GiB limit.

Reproduce basic validation:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python -m unittest -v test_models.py
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python run_initial.py
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python crosscheck_certificates.py
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python large_d_certificates.py --g 1/100
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python check_large_d.py
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python commuting_control.py

Existing checkpoint files are reused. Keep model/certificate metadata with any copied result. Partial sparse spectra are diagnostics only and are not substituted for thermal traces.
